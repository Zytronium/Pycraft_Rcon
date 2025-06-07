#!/bin/python3
"""
Run this file to initiate the Nuclear Mayhem minigame.
This script will initiate the Nuclear Mayhem minigame, and in the case that it encounters an error, it will try to recover.
Custom parameters have been set. You are free to adjust them.

This script exists alongside main.py so that you can run multiple gamemodes at the same time.
"""
from mcrcon import MCRconException
from pycraftCommands import printmc
from time import sleep
from presets import nuclear_mayhem

# PARAMETER CONSTANTS
WRNING_TM = (15, 60)  # How many seconds in advance a warning msg is sent in chat before the nuke falls (can be a range (tuple) )
STRK_INTRVL = 120     # How much time in between nuclear strikes in seconds
INTRVL_VAR = 150      # How much variation in the strike interval (in seconds)
TRGT_MD = "all"    # Targeting mode. Valid values: "random" (targets a random player), "all" (targets all players), or "several_random" (targets multiple random players)

# RECOVERY SETTINGS
RECOVERY_WAIT = 5  # Amount of time to wait before attempting to recover.

if __name__ == '__main__':
    first_try = True
    while True:
        try:
            if not first_try:
                printmc("An error has occurred during Nuclear Mayhem. Attempting to recover...", "red", itallic=True)
                sleep(0.25)
            first_try = False
            nuclear_mayhem(warning_time=WRNING_TM, strike_interval=STRK_INTRVL,
                           interval_variation=INTRVL_VAR, target_mode=TRGT_MD)

        except MCRconException:
            sleep(RECOVERY_WAIT)  # the exception is likely a timeout error caused by server lag. Sleep for a few seconds to try to wait out the lag.
            # Do nothing with MCRcon; this takes us back to the start of the loop
