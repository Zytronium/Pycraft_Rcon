#!/bin/python3
"""This module contains presets for things created using a series of commands, like minigames."""
from pycraftCommands import *


def hello_world():
    printmc("<Pycraft> Hello world!", "gold")
    sleep(3)
    printmc("<World> Hello!")

def death_swap(interval: int = 300, warningMsg: str = None, warningMsgType: str = "chat", warningMsgAdvance: int = 30, countdown: int = None, announceSwap: bool = True, announceSwapPartners: bool = True, randomCreepers: bool = False):
    """
    Death Swap. Every x amount of seconds, everyone's position gets swapped with a random player's
    :param interval: number of seconds between each swap
    :param warningMsg: message to display before each swap
    :param warningMsgType: method of displaying the warning message. "chat" for it to print to public chat. "display" for it to display as a title on each player's screen.
    :param warningMsgAdvance: amount of time in advance the warning message displays before the swap happens
    :param countdown: number of seconds to count down before the swap. Set to None to disable
    :param announceSwap: whether to announce it is swapping when it's time to swap and the countdown hits 0
    :param announceSwapPartners: whether to announce who is swapping with who when the timer hits 0
    :param randomCreepers: every second has a chance to summon a creeper on everyone
    :return:
    """
    # death swap loop
    while True:
        swap_timer = interval
        # timer loop
        while swap_timer >= 0:
            # display warning message if it's time
            if warningMsg is not None and swap_timer == warningMsgAdvance:
                if warningMsgType == "chat":
                    printmc(warningMsg, "yellow", True)
                elif warningMsgType == "display":
                    clear_display("@a")
                    display("@a", fancy_text(warningMsg, "yellow", True), "title")
            # countdown
            if countdown is not None and  0 < swap_timer <= countdown:
                color = "gold" if swap_timer > 3 else "red"
                send_cmd_str("/execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~")
                if swap_timer <= 3:
                    send_cmd_str(
                        "/execute as @a at @s run playsound minecraft:block.note_block.cow_bell master @s ~ ~ ~ 0.25")
                printmc(swap_timer, color, True)

            # announce swap or print the final 0
            if swap_timer == 0:
                if announceSwap:
                    printmc("Swapping...", "light_purple", True)
                elif countdown is not None == 0:
                    printmc("0", "red", True)
            else:  # skip sleeping the last second
                sleep(1)
            swap_timer -= 1
            if randomCreepers and random.randint(0, 245) == 45:
                for player in get_player_list():
                    summon("creeper", player)

        # timer hits 0; swap all players
        swap_all_players(announceSwapPartners)
        if announceSwap or announceSwapPartners:
            send_cmd_str("/execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~")

def nuclear_mayhem(
        target_mode: str = "all",
        # Options: "random", "all", or "several_random"
        warning_time: int = (20, 40),
        # Single integer or tuple range for warning time
        strike_interval: int = 120,
        # Base time in seconds between strikes
        interval_variation: int = 45
        # Amount of variation allowed in strike intervals
):
    """
    Initiates a mini-game where players must shelter from periodic nuclear strikes.

    :param target_mode: "random" (targets a random player), "all" (targets all players), or "several_random" (targets multiple random players)
    :param warning_time: Either an integer or a tuple (min, max) for the countdown warning time
    :param strike_interval: Approximate time (in seconds) between nuclear strikes
    :param interval_variation: Range within which the interval between strikes can vary
    """
    def schedule_next_strike():
        # Calculate the time for the next strike within given interval and variation
        return strike_interval + random.randint(-interval_variation, interval_variation)

    def choose_targets():
        players = get_player_list()
        if target_mode == "random":
            return "@r"
        elif target_mode == "all":
            return "@a"
        elif target_mode == "several_random":
            # Choose multiple unique players to target
            num_targets = max(1, random.randint(1, len(players) // 2))
            return random.sample(players, num_targets)

    def initiate_nuke(target, delay):
        # Offset target coordinates for accuracy

        # Start countdown and execute nuke
        nuke_countdown(target, delay=delay)

    # Main loop for scheduling nuclear strikes
    while True:
        # Determine warning time for each target (fixed or within range)
        delay = warning_time
        if isinstance(warning_time, tuple):
            delay = random.randint(warning_time[0], warning_time[1])

        time_to_next_strike = schedule_next_strike()
        print(f"Next nuclear strike in approximately {time_to_next_strike} seconds.")

        # Wait until the next strike time
        sleep(max(5, time_to_next_strike - delay))

        # Determine targets for the current strike
        targets = choose_targets()
        print(f"Nuclear strike targeting: {targets}")

        # Execute nuke countdown on all targets.
        initiate_nuke(targets, delay)
