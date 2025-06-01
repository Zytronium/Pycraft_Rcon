#!/bin/python3
"""
Run this file to initiate the Nuclear Mayhem minigame.
This script will initiate the Nuclear Mayhem minigame, and in the case that it encounters an error, it will try to recover.
Custom parameters have been set. You are free to adjust them; just be sure to adjust the parameter constants at the top
instead of the function calls at the bottom to ensure they don't change when the script recovers from an error.

This script exists alongside main.py so that you can run multiple gamemodes at the same time.
"""
from mcrcon import MCRconException
from pycraftCommands import printmc
from time import sleep
from presets import nuclear_mayhem

# PARAMETER CONSTANTS
WRNING_TM = (15, 60)  # How many seconds in advance a warning msg is sent in chat before the nuke falls (can be a range (tuple) )
STRK_INTRVL = 300     # How much time in between nuclear strikes in seconds
INTRVL_VAR = 60       # How much variation in the strike interval (in seconds)
TRGT_MD = "random"    # Targeting mode. Valid values: "random" (targets a random player), "all" (targets all players), or "several_random" (targets multiple random players)

if __name__ == '__main__':
    while True:
        try:
            nuclear_mayhem(warning_time=WRNING_TM, strike_interval=STRK_INTRVL,
                           interval_variation=INTRVL_VAR, target_mode=TRGT_MD)
        except MCRconException:
            sleep(10)  # the exception is likely a timeout error caused by server lag. Sleep for 10 seconds to try to wait out the lag.
            printmc("An error has occurred during Nuclear Mayhem. Attempting to recover...", "red", itallic=True)
            sleep(3)  # an additional 3 seconds here doesn't hurt
            nuclear_mayhem(warning_time=WRNING_TM, strike_interval=STRK_INTRVL,
                           interval_variation=INTRVL_VAR, target_mode=TRGT_MD)
