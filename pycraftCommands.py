#!/bin/python3
"""Module for python functions that perform Minecraft commands and send them to a running minecraft server via rcon"""
import re
import random
from random import randint
from time import sleep
from numbers import Number
from sendToServer import send_cmd_str, send_commands_to_minecraft, NUKE_CMD


def fancy_time(seconds: int, round_minutes_to: int | float = 1, round_seconds_to: int = 1, min_round_sec_to_min: int = 51) -> str:
    """
    Convert seconds to either seconds or minutes.
    :param seconds: number of seconds
    :param round_minutes_to: round minutes to the nearest specified minute increment
    :param round_seconds_to: round seconds to the nearest specified second increment
    :param min_round_sec_to_min: minimum number of seconds to convert to minutes instead of seconds
    :return: formatted time string in either minutes or seconds
    """
    if seconds >= min_round_sec_to_min:  # Convert to minutes when seconds exceed 1 minute
        # Convert seconds to minutes and round to the nearest specified minute increment
        minutes = round((seconds / 60) / round_minutes_to) * round_minutes_to
        minutes_str = f"{int(minutes) if minutes.is_integer() else minutes} minute{'s' if minutes != 1 else ''}"
        return minutes_str
    else:
        # Round seconds to the nearest specified second increment
        rounded_seconds = round(seconds / round_seconds_to) * round_seconds_to
        return f"{rounded_seconds} second{'s' if rounded_seconds != 1 else ''}"

def fancy_text(text: str = "", color: str = "white", bold: bool = False, itallic: bool = False, underlined: bool = False, strikethrough: bool = False, obfuscated: bool = False):
    """
    returns the formatted Json text version of the given text.
    Support for links and other fun stuff coming soon. Maybe.
    :param text: text to format
    :param color: color to give it.
    :param bold: set as true to make text bold
    :param itallic: set as true to make text italic
    :param underlined: set as true to make text underlined
    :param strikethrough: set as true to make text strikethrough
    :param obfuscated: set as true to make text obfuscated
    :return: fancy formatted text
    """
    return f"{{\"text\":\"{text}\",\"color\":\"{color}\",\"bold\":{bold},\"italic\":{itallic},\"underlined\":{underlined},\"strikethrough\":{strikethrough},\"obfuscated\":{obfuscated}}}"

def printmc(msg: str = "", color: str = "white", bold: bool = False, itallic: bool = False, underlined: bool = False, strikethrough: bool = False, obfuscated: bool = False):
    """
    Sends a message to the server chat using /tellraw command.
    :param msg: message to send to chat
    :return: /say command output
    """
    if color != "white" or bold or itallic or underlined or strikethrough or obfuscated:
        return send_cmd_str(f"/tellraw @a {fancy_text(msg, color, bold, itallic, underlined, strikethrough, obfuscated)}")
    else:
        return send_cmd_str(f"/tellraw @a \"{msg}\"")

def give(player: str, item: str,  amount: int = 1, item_data: str = "", item_prefix: str = "minecraft:"):
    """
    gives a player an item using the /give command.
    :param player: name of player to give the item(s) to
    :param item: item to give to the player. (prefix is taken care of automatically)
    :param amount: number of items to give to the player
    :param item_data: item data (i.e. "[minecraft:item_name="some_custom_name"]") (including the "[]")
    :param item_prefix: item prefix ("minecraft:" by default if left unspecified)
    :return: command output
    """
    return send_cmd_str(f"/give {player} {item_prefix}{item}{item_data} {amount}")

def teleport(entity: str, *args, **kwargs):
    """
    teleports an entity using the /teleport (aka /tp) command
    :param entity: entity to teleport
    :param args: args
    :param kwargs: key-word args
    :return: command output text
    """
    # Case 1: Teleport to a player (1 positional argument for 'to')
    if len(args) == 1 and isinstance(args[0], str):
        to = args[0]
        return send_cmd_str(f"/teleport {entity} {to}")

    # Case 2: Teleport to specific coordinates (3 positional arguments for x, y, z)
    elif len(args) == 3 and all(isinstance(arg, Number) for arg in args):
        x, y, z = args

        # Check for optional facing coordinates in **kwargs
        if {'facingX', 'facingY', 'facingZ'}.issubset(kwargs):
            facingX, facingY, facingZ = kwargs['facingX'], kwargs['facingY'], kwargs['facingZ']
            return send_cmd_str(
                f"/teleport {entity} {x} {y} {z} facing {facingX} {facingY} {facingZ}")

        # Check for optional facing entity in **kwargs
        elif 'facingEntity' in kwargs and isinstance(kwargs['facingEntity'], str):
            facingEntity = kwargs['facingEntity']
            return send_cmd_str(
                f"/teleport {entity} {x} {y} {z} facing entity {facingEntity}")

        # No facing direction provided
        else:
            return send_cmd_str(f"/teleport {entity} {x} {y} {z}")

    else:
        raise ValueError("Invalid arguments for teleport function")

def swap(entity1: str, entity2: str, announceSwapPartners: bool = False):
    """
    Swaps the positions of two given entities using the /teleport command.
    :param entity1: first entity's UUID or player name
    :param entity2: second entity's UUID or player name
    :param announceSwapPartners: whether to announce who is swapping with who
    """
    at_r_used = False

    # safely set entity1 as a random player if @r was used
    if entity1 == "@r":
        at_r_used = True
        entity1 = get_random_player()
    # safely set entity2 as a random player if @r was used
    if entity2 == "@r":
        at_r_used = True
        entity2 = get_random_player()

    # ensure @a is not used
    if "@a" in [entity1, entity2]:
        raise ValueError("Cannot use @a for this operation. If you wish to swap all players randomly, try swap_all_players()")
    # ensure @e is not used
    if "@e" in [entity1, entity2]:
        raise ValueError("Cannot use @e for this operation.")

    # if @r was used for either entity, the same player was chosen for both entities, and more than 1 player are online:
    if at_r_used and len(get_player_list()) > 1 and entity1 == entity2:
        # reroll entity2 until it's not the same player as entity1
        while entity1 == entity2:
            entity2 = get_random_player()

    # get coords for entity1
    entity_1_pos_x, entity_1_pos_y, entity_1_pos_z = get_entity_coordinates(entity1)
    entity_1_dimension = get_entity_dimension(entity1)
    # coords for entity 2 are not needed

    if announceSwapPartners:
        printmc(f"{entity1} has swapped with {entity2}.", "green", False, True)

    commands = []
    # teleport entity1 to entity2
    commands.append(f"teleport {entity1} {entity2}")
    # Teleport entity2 to entity1's position and dimension
    commands.append(f"execute in {entity_1_dimension} run tp {entity2} {entity_1_pos_x} {entity_1_pos_y} {entity_1_pos_z}")

    # execute commands and swap both players
    send_commands_to_minecraft(command_list=commands)

def swap_all_players(announce_swap_partners: bool = False):
    """
    Swaps each player's position with another player's position, ensuring that each player is swapped
    exactly once. If there's an odd number of players, the last player will be swapped with a random
    player from the list.
    :param announce_swap_partners: whether to announce who is swapping with who
    :return: dict of every player who swapped and who they swapped with
    """
    player_list = get_player_list()
    random.shuffle(player_list)
    swap_dict = {}

    # If there's an odd number of players, set aside the last player
    if len(player_list) % 2 != 0:
        last_player = player_list.pop()
    else:
        last_player = None

    # Pair up players and swap them
    for i in range(0, len(player_list), 2):
        player1, player2 = player_list[i], player_list[i + 1]  # pair players
        swap(player1, player2, announce_swap_partners)  # swap players
        swap_dict[player1] = player2  # add player and swap partner to dict
        swap_dict[player2] = player1  # again but reversed so you can look up either player by the key

    # If there was an odd player out, swap them with a random player from the paired list
    # Note that this can make the swap_dict entry for their partner inaccurate
    if last_player and len(player_list) != 0:  # 0 means 1 player is online because we popped the last player from this list earlier if last_player isn't None
        random_player = random.choice(player_list)
        swap(last_player, random_player, announce_swap_partners)
        swap_dict[last_player] = random_player
        swap_dict[random_player] = last_player
    elif len(player_list) == 0 and announce_swap_partners:
        printmc("Unable to swap. Not enough players.", "green", False, True)

    return swap_dict

def display(player: str, text: str, type: str):
    """
    displays a title on the player's screen
    :param player: player name to display the title to
    :param text: text to display
    :param type: type of title display (i.e. "title," "subtitle,", "actionbar," etc.)
    :return: command output
    """
    send_cmd_str(f"/title {player} {type} \"{text}\"")

def reset_display(player: str):
    """
    resets the title for given player using /title {player} reset.
    don't ask what the difference between clear and reset is. (I don't know)
    :param player: player name to reset the title display for
    :return: command output
    """
    return send_cmd_str(f"/title {player} reset")

def clear_display(player: str):
    """
    clears the title for given player using /title {player} clear.
    don't ask what the difference between clear and reset is. (I don't know)
    :param player: player name to clear the title display for
    :return: command output
    """
    return send_cmd_str(f"/title {player} clear")

def run(*args):
    """
    Run any function. Just type out the command as one string or pass arguments
    in the order they would go based on the game's command syntax
    :param args: command and/or it's arguments (with no leading "/")
    :return: command output
    """
    cmd = "/"
    for arg in args:
        cmd += str(arg) + " "
    return send_cmd_str(cmd)

def execute(entity: str, command: str, *args, **kwargs):
    """
    Executes a command as the specified entity using the /execute command.
    :param entity: The entity to execute the command as.
    :param command: The command to execute.
    :param args: Positional arguments for the command.
    :param kwargs: Keyword arguments for additional options.
    :return: Command output text.
    """
    # Prepare the command string with positional args
    if args:
        arg_str = ' '.join(map(str, args))
        command_str = f"{command} {arg_str}"
    else:
        command_str = command

    # Check if there are any conditions to include from kwargs
    if kwargs:
        conditions = ' '.join([f"{key}={value}" for key, value in kwargs.items()])
        command_str = f"{command_str} {conditions}"

    # Final command
    final_command = f"/execute as {entity} run {command_str}"
    return send_cmd_str(final_command)

def spread_players(radius: int = 20000000, give_regen: bool = False):
    """
    randomly teleports all players around the map
    :param radius: the radius in blocks around 0, 0 that players can be teleported to. Default is 20 million.
    :param give_regen: gives players instant health and saturation to reset them to max. Default is False.
    """
    # Apply effects to all players
    send_cmd_str("/effect give @a minecraft:resistance 20 255 true")  # prevent fall damage
    if give_regen:
        send_cmd_str("/effect give @a minecraft:instant_health 5 255 true")  # restore to max hp
        send_cmd_str("/effect give @a minecraft:saturation 5 255 true")  # restore to max saturation
    player_list = get_player_list()

    # Teleport to random coordinates, at build limit, within the specified radius
    for player in player_list:
        x = randint(-radius, radius)
        y = 319
        z = randint(-radius, radius)
        teleport(player, x, y, z)
        # printmc(f"Setting spawnpoint for {player} to {int(x)} {50} {int(z)}")
        # send_cmd_str(f"/spawnpoint {player} {int(x)} {50} {int(z)}")

def clear_all(override_confirmation: bool = False):
    """
    Clears the inventories of all players.
    :return: command output
    """
    if not override_confirmation:
        # confirm clear all inventories
        user_input = input(
            f"Are you sure you want to clear ALL players' inventories? " +
            "This is a risky operation. [Y/N]: ").lower().strip()

        # clear all inventories
        if user_input == 'y':
            return send_cmd_str("/clear @a")

        # abort
        elif user_input == "n":
            print("Operation canceled.")
            return

    # else if override is True, skip confirmation and clear all inventories
    return send_cmd_str("/clear @a")

def op(player: str):
    """
    Makes then given player a server operator. This is a risky operation.
    :param player: name of player to grant operator permissions
    :return: /op command output
    """
    while True:
        user_input = input(
            f"Are you sure you want to op {player}? " +
            "This is a risky operation. [Y/N]: ").lower().strip()

        if user_input == "y":
            output = send_cmd_str(f"/op {player}")
            print(output)
            return output

        elif user_input == "n":
            print("Operation canceled.")
            return

        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def deop(player: str):
    """
    Makes then given player no longer a server operator.
    :param player: name of player to revoke operator permissions
    :return: /deop command output
    """
    output = send_cmd_str(f"/deop {player}")
    print(output)
    return output

def set_weather(type: str, duration: int = None, duration_unit: str = ""):
    """
    Sets the weather to the specified type for the given duration.
    :param type: type of weather to set
    :param duration: duration to keep the weather at. Or blank
    :param duration_unit: Unit of time for duration. "t" (ticks) is default if left blank
    :return: command output
    """
    # ensure weather type is valid
    if type not in ["clear", "rain", "thunder"]:
        raise ValueError("Invalid weather type. Type must be \"clear\", \"rain\", or \"thunder\"")
    # ensure duration given is a positive integer
    if duration is not None and duration <= 0:
        raise ValueError("Invalid duration. Duration must be greater than 0")
    # ensure duration unit is valid
    if duration_unit.lower() not in ["", "t", "s", "d"]:
        raise ValueError("Invalid duration unit. Duration unit must be \"t\" (ticks), \"s\" (seconds), or \"d\" (days)\"")

    return send_cmd_str(f"/weather {type} {duration if duration is not None else ''}{duration_unit.lower() if duration is not None else ''}")

def summon(entity_type: str, *args, dimension: str = None, custom_prefix: str = "minecraft:", custom_data: dict = None, amount: int = 1, return_command: bool = False, **kwargs):
    """
    Summons an entity at specified coordinates or at a given entity's position.

    :param entity_type: The type of entity to summon (e.g., 'creeper').
    :param args: Either a single entity (UUID, player name, or selector) or x, y, z coordinates.
    :param dimension: the dimension to summon it in
    :param custom_prefix: Optional custom prefix for the entity (default is "minecraft:").
    :param custom_data: Optional custom entity data as a dictionary.
    :param amount: The number of entities to spawn (default is 1).
    :param return_command: If True, return the summon command as a string instead of sending it.
    :param kwargs: Optional keyword arguments for additional flexibility (e.g., tags or other data).
    :return: Command output from the last command used to summon the entity/entities (if run) or the command string (if return_command is True)
    """
    # set default dimension if left as None and no entity given
    if len(args) != 1 and dimension is None:
        dimension = "minecraft:overworld"

    # Automatically handle the prefix
    entity_type = f"{custom_prefix}{entity_type}"

    # Check if args length is valid
    if len(args) == 1:
        target_entity = args[0]
        x, y, z = get_entity_coordinates(target_entity)
        dimension = get_entity_dimension(target_entity)
        if x is None or y is None or z is None or dimension is None:
            print("Entity not found or invalid location.")
            return None
    elif len(args) == 3:
        x, y, z = args
    else:
        print("Invalid arguments: Provide either a single target entity or x, y, z coordinates.")
        return None

    # Build the summon command
    summon_command = f"/execute in {dimension} run summon {entity_type} {x} {y} {z}"

    # Handle custom entity data if provided
    if custom_data:
        data_tags = ', '.join(f'{key}:{value}' for key, value in custom_data.items())
        summon_command += f" {{{data_tags}}}"

    # Add any additional kwargs as data tags if provided
    if kwargs:
        data_tags = ', '.join(f'{key}:{value}' for key, value in kwargs.items())
        summon_command += f" {{{data_tags}}}"

    if return_command:
        return [summon_command] * amount

    output = ""
    for _ in range(amount):
        output = send_cmd_str(summon_command)

    return output

def smite(entity: str):
    """
    strikes the given entity with a bolt of lightning.
    They probably deserved it anyway.
    :param entity: the player or entity to smite
    :return: command output
    """

    return summon("lightning_bolt", entity)

def smite_all():
    """
    strikes every player with a bolt of lightning.
    That'll teach them to behave! Bow before your leader!
    :return: command output
    """
    for player in get_player_list():
        smite(player)

def explode(entity: str):
    """
    blows up the given player (death not guaranteed)
    :param entity: the player or entity to spontaneously combust
    :return: command output
    """
    return summon("tnt", entity)

def nuke(entity: str, missile_mode: bool = False, power: int = 127, spread: int = 3, coords: tuple = None, return_commands: bool = False):
    """
    Drops nuclear fireballs on a given player, causing death and destruction
    :param entity: the player or entity to nuke
    :param spread: how spread out the fireballs creating the nuke can be. Default is 3
    :param coords: the coordinates to nuke at, or None if nuking the entity instead
    :param return_commands: if True, return a list of command strings instead of sending them. Default: False
    :return: None or list of command strings
    """
    # Set to true if the server has a /nuke command compatible with this function
    use_server_nuke_cmd = True if NUKE_CMD != False else False
    use_coords = isinstance(coords, tuple) and len(coords) == 3

    if entity == "@r":
        entity = random.choice(get_player_list())

    if use_server_nuke_cmd:
        cmd = f"{NUKE_CMD} {entity} {missile_mode}"
        if return_commands:
            return [cmd]
        return send_cmd_str(cmd, cmd_prefix="")

    commands = []

    for i in range(0, 4):
        x, y, z = coords if use_coords else get_entity_coordinates(entity)
        x += randint(spread * -1, spread)
        y += randint(-3, 3) if not missile_mode else max(345, y + 425)  # if missile mode, summon it at a height calculated to impact the ground in roughly 5 seconds
        z += randint(spread * -1, spread)
        nuke_data = {
        "Motion": [0.0, -10.0, 0.0],       # Extreme downwards velocity
        "ExplosionPower": min(power, 127), # Large explosion radius
        "CustomName": "\"nuke\""           # Name the fireball "nuke"
    }

        commands.extend(
            summon("fireball", x, y, z, dimension=get_entity_dimension(entity),
                   custom_data=nuke_data, return_command=True))

    if return_commands:
        return commands
    for cmd in commands:
        send_cmd_str(cmd)

    return None

def orbital_laser(entity: str, intensity: float = 15.0, coords: tuple = None):
    """
    Fires an orbital laser beam on the given player, causing death and destruction
    :param entity: the player or entity to strike
    :param intensity: intensity of the blast. Default: 15.0
    :param coords: the coordinates of the blast, or None if striking the entity instead
    """
    use_coords = True if isinstance(coords, tuple) and len(coords) == 3 else False

    if entity == "@r":
        entity = random.choice(get_player_list())

    x, y, z = map(int, coords if use_coords else get_entity_coordinates(entity))

    commands = []

    # Charge actionbar and initial sound
    commands.append(f"/execute as {entity} at @s run title @s actionbar {{\"text\":\"⚠ ORBITAL STRIKE CHARGING ⚠\",\"color\":\"red\",\"bold\":true}}")
    commands.append("/execute as @a at @s run playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 1")
    send_commands_to_minecraft(command_list=commands)

    # Charging visuals every 0.5 seconds for 5 seconds (10 ticks)
    for _ in range(10):
        charging_tick_cmds = [
            f"/execute positioned {x} {y} {z} run particle dust{{color:[1.0,1.0,0.2],scale:2}} {x} {y + 3} {z} 0 200 0 0.05 500 force"
        ]
        send_commands_to_minecraft(command_list=charging_tick_cmds)
        sleep(0.5)

    # Blast effect
    blast_cmds = [
        f"/execute positioned {x} {y} {z} run fill {x - 5} {y - 8} {z - 5} {x + 5} {y + 85} {z + 5} air replace water",
        f"/execute positioned {x} {y} {z} run fill {x - 2} {y - 4} {z - 2} {x + 2} {y + 80} {z + 2} air replace lava",
        f"/execute positioned {x} {y} {z} run fill {x - 1} {y - 1} {z - 1} {x + 1} {319} {z + 1} air destroy",
        f"/execute positioned {x} {y} {z} run particle flash {x} {y} {z} 0 -35 0 0 500000 force",
        f"/execute positioned {x} {y} {z} run particle dust{{color:[1.0,0.25,0.25],scale:4}} {x} {y + 100} {z} 0 -35 0 0 50000 force",
        "/execute as @a at @s run playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 1",
        "/execute as @a at @s run playsound minecraft:entity.warden.sonic_boom master @s ~ ~ ~ 2 1",
        f"/execute positioned {x} {y} {z} run playsound minecraft:entity.generic.explode master @a ~ ~ ~ 1 ",
        "/execute as @a run playsound minecraft:entity.generic.explode master @a ~ ~ ~ 1 1",
        "/execute as @a run playsound minecraft:entity.lightning_bolt.thunder master @a ~ ~ ~ 10 0.25",
        "/execute as @a run playsound minecraft:entity.lightning_bolt.thunder master @a ~ ~ ~ 10 1.9",
        f"/execute positioned {x} {y} {z} run particle explosion_emitter {x} {y + 11} {z} 0 -10 0 0 50 force",
        f"/execute positioned {x} {y} {z} run particle explosion_emitter {x} {y + 11} {z} 4 -1 -4 0 50 force",
        f"/execute positioned {x} {y} {z} run particle explosion_emitter {x} {y + 11} {z} -4 -1 4 0 50 force",
        f"/execute positioned {x} {y} {z} run summon lightning_bolt {x} {y-1} {z}",
        f"/execute positioned {x} {y} {z} run summon area_effect_cloud {x} {y-1} {z} {{Radius:15f,Duration:130,Particle:\"smoke\"}}",
        f"/execute positioned {x} {y} {z} run summon area_effect_cloud {x} {y+2} {z} {{Radius:10f,Duration:110,Particle:\"smoke\"}}",
        f"/execute positioned {x} {y} {z} run summon area_effect_cloud {x} {y+3} {z} {{Radius:3f,Duration:100,Particle:\"smoke\"}}",
        f"/execute as @e positioned {x} {y} {z} if entity @s[distance=..2] run damage @s 5000 minecraft:generic"
    ]

    base_damage = intensity * 10
    max_radius = int(intensity * 10)
    radial_damage_cmds = [f"/execute as @e positioned {x} {y} {z} if entity @s[distance=..2] run damage @s 5000 minecraft:generic"]

    for r in range(1, min(255, max_radius + 1)):
        # scale damage down by distance
        damage = max(1, int(base_damage / (r * 1.5)))

        radial_damage_cmds.append(f"/execute as @e at @s if entity @s[distance={r}..{r+1}] run damage @s {damage} minecraft:generic")
    if max_radius > 256:
        radial_damage_cmds.append(f"/execute as @e at @s if entity @s[distance={255}..{max_radius}] run damage @s 1 minecraft:generic")

    blast_cmds.extend(radial_damage_cmds)

    # create additional explosions
    for i in range(0, min(50, int(intensity / 15) + 1)):
        blast_cmds.extend(nuke(entity, power=int(intensity), spread=int(intensity / 3), coords=(x, y, z), return_commands=True))

    send_commands_to_minecraft(command_list=blast_cmds)


    # add a bit of fire if the previous explosions were too weak to create much fire.
    summon("fireball", entity, custom_data={"Motion": [0.0, -10.0, 0.0]})



def list_players():
    """
    Lists all currently connected players using the /list command.
    :return: Command output text.
    """
    return send_cmd_str("/list")

def list_player_uuids():
    """
    Lists all currently connected players using the /list command.
    :return: Command output text.
    """
    return send_cmd_str("/list uuids")

def get_player_list():
    """
    Returns a list of online player names without the prefix text from the /list command.
    :return: List of player names.
    """
    # Get the full output of the /list command
    output = send_cmd_str("/list")

    # Find the part of the output after the last colon and strip any whitespace
    players_text = output.split(":")[-1].strip()

    # Split the names by comma and strip extra whitespace from each name
    player_list = [player.strip() for player in players_text.split(",") if
                   player.strip()]

    return player_list

def get_uuid_list():
    """
    Returns a list of UUIDs of online players without the prefix text from the /list uuids command.
    :return: List of UUIDs as strings.
    """
    # Get the full output of the /list uuids command
    output = list_player_uuids()  # Assuming list_player_uuids() sends "/list uuids" and returns the output

    # Use regex to find all UUIDs within parentheses
    uuid_list = re.findall(r'\(([^)]+)\)', output)

    return uuid_list

def get_player_uuid_dict():
    """
    Returns a dictionary where each player's name is a key and their UUID is the corresponding value.
    This function assumes the number of players returned by get_player_list() matches
    the number of UUIDs returned by get_uuid_list().

    :return: Dictionary of player names as keys and UUIDs as values
    """
    # Get the list of players and UUIDs
    player_list = get_player_list()
    uuid_list = get_uuid_list()

    # Ensure both lists are the same length to avoid mismatches
    if len(player_list) != len(uuid_list):
        raise ValueError("Mismatch between the number of players and UUIDs.")

    # Create dictionary by zipping player names and UUIDs
    player_uuid_dict = dict(zip(player_list, uuid_list))

    return player_uuid_dict

def get_entity_coordinates(entity: str):
    """
    Gets the X, Y, Z coordinates of a given entity.
    :param entity: The entity whose coordinates are being queried.
    :return: A tuple (x, y, z) of coordinates, or None if the entity is not found.
    """
    # Run the command to get the entity's position
    output = send_cmd_str(f"/data get entity {entity} Pos")

    # Use regex to extract the three floating-point or scientific notation coordinates from the output
    match = re.search(r'\[([\-?\d\.eE]+)d, ([\-?\d\.eE]+)d, ([\-?\d\.eE]+)d\]', output)

    if match:
        # Convert matched groups to floats (handling scientific notation automatically) and return as a tuple
        x, y, z = map(float, match.groups())
        return x, y, z
    else:
        # If the entity is not found or an error occurs, return None
        return None

def get_entity_dimension(entity):
    """
    Gets the current dimension of the given entity.
    :param entity: name or UUID of the entity.
    :return: the dimension the entity is in.
    """
    response = send_cmd_str(f"/data get entity {entity} Dimension")

    if response:
        print(response)
    else:
        print("Error getting response.")

    dimension_match = re.search(r'"([\w:]+)"', response)

    if dimension_match:
        dimension = dimension_match.group(1)
        return dimension
    else:
        print(
            f"Could not find dimension information for entity {entity}.",
            "red")
        return None

def get_random_player():
    return get_player_list()[random.randint(0, len(get_player_list()) - 1)]

def troll_all_players():
    """
    Trolls all players by doing a fake random giveaway, then giving everyone a
    fake prize & instructing them to alt+F4 to claim a minute of creative mode
    """
    printmc("Attention all players! In 15 seconds, a random player will be " +
            "picked to win a free prize! The winner will be discretely " +
            "messaged instructions on how to claim it. Good luck!")
    sleep(15)
    printmc("A winner has been chosen! Congratulations if you won!")
    send_cmd_str("/tell @a \"Congratulations! You have won the grand prize of " +
    "3 stacks of god apples, and 1 minute of free creative mode! To enter " +
    "creative mode, please do alt+F2, then alt+F3 then alt+F4.\"")
    give("@a", "poisonous_potato", 192,
         "[minecraft:item_name='{\"text\":\"Death Apple\"}',minecraft:item_model=enchanted_golden_apple,minecraft:enchantment_glint_override=true,minecraft:rarity=rare]")
    give("@r", "rotten_flesh", 64)

def herobrine(lightning: bool = True):
    """makes Herobrine join the game"""
    printmc("Herobrine joined the game", "yellow")
    if lightning:
        summon("lightning_bolt", 0, 40, 0)

def sudo(playername: str, message: str, override_name_check: bool = False):
    if not override_name_check and playername not in get_player_list():
        while True:
            user_input = input("That player is not online. Send message anyway? [Y/N]: ").lower().strip()
            if user_input == "y":
                break  # continue and print sudo message
            elif user_input == "n":
                print("Operation canceled.")
                return  # abort

    printmc(f"<{playername}> {message}")

def self_destruct(countdown: int = 10):
    # Ensure countdown is at least 1 second
    if countdown < 1:
        raise ValueError("Countdown must be a positive number.")

    # Warning message
    printmc("WARNING: THE SERVER\'S SELF DESTRUCT SEQUENCE HAS BEEN ACTIVATED. THE SERVER WILL SHUT DOWN IN...", "red", True)

    # Countdown sequence
    while countdown > 0:
        color = "yellow" if countdown > 3 else "red"
        send_cmd_str("/execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~")
        if countdown <= 3:
            send_cmd_str(
                "/execute as @a at @s run playsound minecraft:block.note_block.cow_bell master @s ~ ~ ~")
        printmc(countdown, color)
        countdown -= 1
        sleep(1)

    # Shutdown message
    printmc("Shutting down server...","gray")
    sleep(0.125)
    send_cmd_str("/stop")

def setup_deathswap(radius: int = 25000000):
    # clear players' inventories
    clear_all(True)

    # ensure all players are in survival mode
    send_cmd_str("/gamemode survival @a")

    # randomly tp players
    spread_players(radius, True)

    # give players food
    give("@a", "golden_carrot", 64)

def nuke_countdown(player: str | list, delay: int = 20, countdown: int = 10):
    if delay < 5:
        raise ValueError("Countdown must be at least 5 seconds to allow for the nuke to drop in sync.")

    mode = "targeted"
    if isinstance(player, list):
        mode = "several"
    elif player == "@r":
        mode = "random"
        player = get_random_player()
    elif player == "@a":
        mode = "all"

    warning_msg = "WARNING: "
    if mode == "targeted":
        warning_msg += "A TARGETED NUCLEAR STRIKE HAS BEEN ORDERED ON AN UNNAMED INDIVIDUAL. "
    elif mode == "random":
        warning_msg += "A NUCLEAR STRIKE IS INCOMING AND HEADED DIRECTLY TOWARDS A RANDOM PLAYER. "
    elif mode == "all":
        warning_msg += "A SERIES OF NUCLEAR STRIKES HAVE BEEN ORDERED ON THIS WORLD. SEEK SHELTER IMMEDIATELY. "
    elif mode == "several":
        warning_msg += "A SERIES OF NUCLEAR STRIKES HAVE BEEN ORDERED ON SEVERAL PEOPLE. SEEK SHELTER IMMEDIATELY. "

    warning_msg += f"THE MISSILE{"S" if mode in ["all", "several"] else ""} WILL IMPACT IN APPROXIMATELY {fancy_time(delay, 1, 5, 95).upper()}. THIS IS NOT A DRILL. "
    if randint(0, 29) == 29:  # 1 in 30 chance of adding a dad joke to the warning
        warning_msg += "IT IS A HAMMER. "

    printmc(warning_msg, "gold", True)
    send_cmd_str(
        "/execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~")

    while delay >= 0:
        sleep(1)
        if delay <= countdown:
            color = "gold" if delay > 3 else "red"
            send_cmd_str(
                "/execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~")
            if delay <= 3:
                send_cmd_str(
                    "/execute as @a at @s run playsound minecraft:block.note_block.cow_bell master @s ~ ~ ~ 0.25")
            printmc(delay, color, True)

        if delay == 5:
            if mode == "targeted" or mode == "random":
                nuke(player, True)
            elif mode == "several":
                for p in player:
                    nuke(p, True)
            else:
                nuke_all()

        delay -= 1

def nuke_all():
    for player in get_player_list():
        sleep(randint(125, 2500) * 0.00001)
        nuke(player, True)

if __name__ == '__main__':
    printmc("Test 123", "gold", True)
