#!/bin/python3
"""This is the main script where you can code what you want to happen in the server"""
from presets import *


def script1():
    player_dict = get_player_uuid_dict()
    print("----------------")
    print(player_dict)
    print("----------------")
    line = "-" * len(str(player_dict))
    printmc(f"Player List Dictionary:\n{line}\n{str(player_dict)}\n{line}")
    sleep(0.125)
    printmc("Teleporting everyone to 15.125, 84, 1...")
    sleep(1)
    teleport("@a", 15.125, 84.0, 1)

    sleep(2)

    printmc("Teleporting everyone to random player...")
    sleep(1)
    teleport("@a", "@r")

    sleep(1)
    smite(get_random_player())
    sleep(1)

    printmc(
        "Teleporting Zytronium to 3 blocks away from some random sheep and facing it...")
    sleep(1)
    teleport("Zytronium", "15e12be1-692f-4c40-9d24-194dfc1af77b")
    x, y, z = get_entity_coordinates("15e12be1-692f-4c40-9d24-194dfc1af77b")
    execute("Zytronium",
            f"tp @s {x + 3} {y} {z} facing entity 15e12be1-692f-4c40-9d24-194dfc1af77b")

    sleep(2)

    printmc("Giving a frien to everyone :D")
    sleep(1)
    for player in get_player_list():
        summon("creeper", player,
               custom_data={"CustomName": '"Frien"', "NoAI": 1}, amount=1)

    sleep(2)

    printmc("Summoning a creep at world spawn...", "green")
    summon("creeper", 0, 64, 0, custom_data={"CustomName": '"Creep"'})

    sleep(10)

    smite(get_random_player())

if __name__ == "__main__":
    # make your script here
    printmc("Pycraft Rcon script running.", "green", True)
    sleep(1)
    hello_world()
    # smite("Zytronium")

    # nuclear_mayhem(strike_interval=20, target_mode="random")

    # setup_deathswap()
    # printmc("Death Swap has initiated. Every 3 minutes, all players will swap with a random player. Good luck!", "dark_aqua", True)
    # death_swap(180, "Warning: 30 seconds until swap.", "chat", 30, 5, True, True, False)



