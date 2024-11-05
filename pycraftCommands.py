#!/bin/python3
"""Module for python functions that perform Minecraft commands and send them to a running minecraft server via rcon"""
import random
import re
from random import randint
from time import sleep
from numbers import Number
from sendToServer import send_cmd_str


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
    :param entity1: first entity UUID or player name
    :param entity2: second entity UUID or player name
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
        printmc(f"Swapping {entity1} with {entity2}...", "dark_green", False, True)

    # teleport entity1 to entity2
    teleport(entity1, entity2)
    # Teleport entity2 to entity1's position and dimension
    send_cmd_str(
        f"/execute in {entity_1_dimension} run tp {entity2} {entity_1_pos_x} {entity_1_pos_y} {entity_1_pos_z}")

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
        player1, player2 = player_list[i], player_list[i + 1]
        swap(player1, player2, announce_swap_partners)
        swap_dict[player1] = player2
        swap_dict[player2] = player1

    # If there was an odd player out, swap them with a random player from the paired list
    if last_player:
        random_player = random.choice(player_list)
        swap(last_player, random_player, announce_swap_partners)
        swap_dict[last_player] = random_player
        swap_dict[random_player] = last_player

    return swap_dict

def display(player: str, text: str, type: str):
    """

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

def spread_players(radius: int = 1000000, give_regen: bool = False):
    send_cmd_str("/effect give @a minecraft:resistance 25 255")
    if give_regen:
        send_cmd_str("/effect give @a minecraft:instant_health 255")
        send_cmd_str("/effect give @a minecraft:saturation 255")
    player_list = get_player_list()

    # Initial teleport to random high altitude within the specified radius
    for player in player_list:
        x = randint(-radius, radius)
        y = 319
        z = randint(-radius, radius)
        teleport(player, x, y, z)
        # printmc(f"Setting spawnpoint for {player} to {int(x)} {50} {int(z)}")
        # send_cmd_str(f"/spawnpoint {player} {int(x)} {50} {int(z)}")

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

def summon(entity_type: str, *args, custom_prefix: str = "minecraft:", custom_data: dict = None, amount: int = 1, **kwargs):
    """
    Summons an entity at specified coordinates or at a given entity's position.

    :param entity_type: The type of entity to summon (e.g., 'creeper').
    :param args: Either a single entity (UUID, player name, or selector) or x, y, z coordinates.
    :param custom_prefix: Optional custom prefix for the entity (default is "minecraft:").
    :param custom_data: Optional custom entity data as a dictionary.
    :param amount: The number of entities to spawn (default is 1).
    :param kwargs: Optional keyword arguments for additional flexibility (e.g., tags or other data).
    :return: The command string used to summon the entity.
    """
    # Automatically handle the prefix
    entity_type = f"{custom_prefix}{entity_type}"

    # Check if args length is valid
    if len(args) == 1:
        target_entity = args[0]
        x, y, z = get_entity_coordinates(target_entity)
        if x is None or y is None or z is None:
            print("Entity not found or invalid coordinates.")
            return None
    elif len(args) == 3:
        x, y, z = args
    else:
        print("Invalid arguments: Provide either a single target entity or x, y, z coordinates.")
        return None

    # Build the summon command
    summon_command = f"/summon {entity_type} {x} {y} {z}"

    # Handle custom entity data if provided
    if custom_data:
        data_tags = ', '.join(f'{key}:{value}' for key, value in custom_data.items())
        summon_command += f" {{{data_tags}}}"

    # Add any additional kwargs as data tags if provided
    if kwargs:
        data_tags = ', '.join(f'{key}:{value}' for key, value in kwargs.items())
        summon_command += f" {{{data_tags}}}"

    # Run the command multiple times if amount > 1
    commands = []
    for _ in range(amount):
        commands.append(summon_command)

    for command in commands:
        print(f"Executing command: {command}")
        # Here, you would typically send the command to the server
        send_cmd_str(command)

    return commands

def smite(entity: str):
    """
    strikes the given entity with a bolt of lightning.
    They probably deserved it anyway.
    :param entity: the player or entity to smite
    :return: command output
    """
    x, y, z = get_entity_coordinates(entity)
    return send_cmd_str(f"/summon minecraft:lightning_bolt {x} {y} {z}")

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
    x, y, z = get_entity_coordinates(entity)
    return send_cmd_str(f"/summon minecraft:tnt {x} {y} {z}")

def nuke(entity: str):
    """
    blows up the given player for long enough to almost guarantee death and destruction
    :param entity: the player or entity to nuke
    """
    for i in range(1, 321):
        x, y, z = get_entity_coordinates(entity)
        x += randint(-3, 3)
        y += randint(-3, 3)
        z += randint(-3, 3)
        send_cmd_str(f"/summon minecraft:tnt {x} {y} {z}")

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
        printmc(f"{entity} is currently in the {dimension} dimension.",
                "gray")
        return dimension
    else:
        printmc(
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

def self_destruct(countdown: int = 10):
    # Ensure countdown is at least 1 second
    if countdown < 1:
        raise ValueError("Countdown must be a positive number.")

    # Warning message
    printmc("WARNING: THE SERVER\'S SELF DESTRUCT SEQUENCE HAS BEEN ACTIVATED. THE SERVER WILL SHUT DOWN IN...", "red", True)

    # Countdown sequence
    while countdown > 0:
        color = "yellow" if countdown >= 5 else "red"
        printmc(countdown, color)
        countdown -= 1
        sleep(1)

    # Shutdown message
    printmc("Shutting down server...","gray")
    sleep(0.125)
    send_cmd_str("/stop")


if __name__ == '__main__':
    printmc("Test 123", "gold", True)
