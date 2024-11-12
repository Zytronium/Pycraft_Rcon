#!/bin/python3
"""
Run this file to initiate the Death Swap minigame.
This script will:
- Setup deathswap
    - Clears everyone's inventories
    - Sets everyone's gamemode to survival mode
    - Randomly teleports players around the map so that they don't interact
    - And gives everyone a stack of food
    - Note: to change the radius that players can be teleported in during rtp:
        - Simply put that value inside the parentheses in "setup_deathswap()"
        - If you are also running Nuclear Mayhem at the same time and wish to make everyone close enough to eachother to hear the nuclear impacts,
        set the radius to around 5000. Thunder from nuclear impacts can be heard from a little over 5,000 blocks away.
- Initiate the Death Swap minigame
    - With all default parameters

This script exists alongside main.py so that you can run multiple gamemodes at the same time.
"""
from presets import death_swap
from pycraftCommands import setup_deathswap


if __name__ == '__main__':
    setup_deathswap()
    death_swap()
