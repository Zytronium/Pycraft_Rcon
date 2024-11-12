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


while True:
    try:
        nuclear_mayhem(warning_time=(15, 45), strike_interval=150,
                       interval_variation=15, target_mode="random")
    except MCRconException:
        printmc("An error has occurred during Nuclear Mayhem. Attempting to recover...", "red", itallic=True)
        sleep(3)
        nuclear_mayhem(warning_time=(15, 45), strike_interval=150,
                       interval_variation=15, target_mode="random")
