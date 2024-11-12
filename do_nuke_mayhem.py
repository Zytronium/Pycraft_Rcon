#!/bin/python3
"""
Run this file to initiate the Nuclear Mayhem minigame.
This script will initiate the Nuclear Mayhem minigame, and in the case that it encounters an error, it will try to recover.
Custom parameters have been set. You are free to adjust them. Be sure to adjust both function calls equally.

This script exists alongside main.py so that you can run multiple gamemodes at the same time.
"""
from mcrcon import MCRconException
from pycraftCommands import printmc
from time import sleep
from presets import nuclear_mayhem

if __name__ == '__main__':
    while True:
        try:
            nuclear_mayhem(warning_time=(15, 45), strike_interval=150,
                           interval_variation=15, target_mode="random")
        except MCRconException:
            sleep(10)  # the exception is likely a timeout error caused by server lag. Sleep for 10 seconds to try to wait out the lag.
            printmc("An error has occurred during Nuclear Mayhem. Attempting to recover...", "red", itallic=True)
            sleep(3)  # an additional 3 seconds here doesn't hurt
            nuclear_mayhem(warning_time=(15, 45), strike_interval=150,
                           interval_variation=15, target_mode="random")
