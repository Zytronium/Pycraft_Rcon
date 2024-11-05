#!/bin/python3
"""This module contains presets for things created using a series of commands, like minigames."""
from pycraftCommands import *


def hello_world():
    printmc("<Pycraft> Hello world!", "gold")
    sleep(3)
    printmc("<World> Hello!")

def death_swap(interval: int = 300, warningMsg: str = None, warningMsgType: str = "chat", warningMsgAdvance: int = 30, countdown: int = None, announceSwap: bool = True, announceSwapPartners: bool = True):
    """
    Death Swap. Every x amount of seconds, everyone's position gets swapped with a random player's
    :param interval: number of seconds between each swap
    :param warningMsg: message to display before each swap
    :param warningMsgType: method of displaying the warning message. "chat" for it to print to public chat. "display" for it to display as a title on each player's screen.
    :param warningMsgAdvance: amount of time in advance the warning message displays before the swap happens
    :param countdown: number of seconds to count down before the swap. Set to None to disable
    :param announceSwap: whether to announce it is swapping when it's time to swap and the countdown hits 0
    :param announceSwapPartners: whether to announce who is swapping with who when the timer hits 0
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

        # timer hits 0; swap all players
        swap_all_players(announceSwapPartners)
