#!/bin/python3
from mcrcon import MCRcon
from sys import argv

# Initialize the variables
RCON_HOST = None
RCON_PORT = None
RCON_PASSWORD = None

# Try to read the connection settings from the file
try:
    with open("connection_settings", 'r') as file:
        for line in file:
            # Strip whitespace and split by colon
            key, value = line.strip().split(':', 1)
            value = value.strip()  # Remove leading/trailing spaces

            if key == "rcon host":
                RCON_HOST = value
            elif key == "rcon port":
                RCON_PORT = int(value)
            elif key == "rcon password":
                RCON_PASSWORD = value
except FileNotFoundError:
    # If the file doesn't exist, create it and write the default content
    with open("connection_settings", 'w') as file:
        file.write("""rcon host: localhost\nrcon port: 25575\nrcon password: change_me""")
    # Set the default values to the variables
    RCON_HOST = "localhost"
    RCON_PORT = 25575
    RCON_PASSWORD = "change_me"

# Path to the file containing Minecraft commands
COMMAND_FILE_PATH = 'commands.txt' if len(argv) < 2 else argv[1]

def send_commands_to_minecraft():
    # Connect to the Minecraft server via RCON
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        # Open the file with the Minecraft commands
        with open(COMMAND_FILE_PATH, 'r') as command_file:
            for command in command_file:
                command = command.strip()  # Remove any trailing whitespace or newline
                if command:
                    mcr.command(command)  # Send the command to the server
                    print(f"Executed: {command}\nServer Response: ", end="")

def send_cmd_str(command: str):
    # Connect to the Minecraft server via RCON
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        # Open the file with the Minecraft commands
        cmd = command.strip()  # Remove any trailing whitespace or newline
        if cmd:
            response = mcr.command(cmd)  # Send the command to the server
            print(f"\nExecuted:\n{cmd}\n\nServer Response: ")
            return response
    return None

if __name__ == '__main__':
    # Run the function
    if len(argv) < 2:
        print("No source file given. Defaulting to 'commands.txt'")
    send_commands_to_minecraft()
