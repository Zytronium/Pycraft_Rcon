#!/bin/python3
from mcrcon import MCRcon
from sys import argv

# Initialize the server connection setting variables
# rcon settings
RCON_HOST = None
RCON_PORT = None
RCON_PASSWORD = None
# server variables
USE_VANILLA_PREFIX = None
NUKE_CMD = None

# Initialize settings variables
CONNECTION_SETTINGS_FILE = None

# Try to read the settings file
try:
    with open("settings/settings", 'r') as settings_file:
        for line in settings_file:
            # Strip whitespace and split by colon
            key, value = line.strip().split(':', 1)
            value = value.strip()  # Remove leading/trailing spaces

            match key:
                case "server connection settings file":
                    CONNECTION_SETTINGS_FILE = f"settings/server_connections/{value}"
                # add more cases here when more settings are added
except FileNotFoundError:
    # If the file doesn't exist, create it and write the default content
    with open("settings/settings", 'w') as file:
        file.write("""server connection settings file: default""")
    # Set the default values to the variables
    CONNECTION_SETTINGS_FILE = "settings/server_connections/default"


# Try to read the connection settings from the file
try:
    with open(CONNECTION_SETTINGS_FILE, 'r') as file:
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
            elif key == "rcon password":
                RCON_PASSWORD = value
            elif key == "require vanilla cmd prefix":
                USE_VANILLA_PREFIX = True if value.lower() == "true" else False
            elif key == "compatible nuke cmd":
                NUKE_CMD = False if value.lower() == "false" else value.replace("/", "")

except FileNotFoundError:
    # If the file doesn't exist, create it and write the default content
    with open("settings/server_connections/default", 'w') as file:
        file.write("""rcon host: localhost\nrcon port: 25575\n""" +
                   """rcon password: change_me\nrequire vanilla cmd prefix: false\n""" +
                   """compatible nuke cmd: false""")
    # Set the default values to the variables
    RCON_HOST = "localhost"
    RCON_PORT = 25575
    RCON_PASSWORD = "change_me"
    USE_VANILLA_PREFIX = False
    NUKE_CMD = False

# Path to the file containing Minecraft commands
COMMAND_FILE_PATH = 'commands.txt' if len(argv) < 2 else argv[1]

def send_commands_to_minecraft(command_file_path: str = None,
                               command_list: list = None):
    """
    sends a series of commands to the minecraft server.
    :param command_file_path: path to the file containing a list of commands,
    organized with one command per line. Must be a string that contains the
    relative path from this program's root directory
    (the parent folder of the file that defines this function) (I think).
    :param command_list: list of commands to send. Must be a list of strings.
    """
    mode = None

    if command_file_path is None:
        if command_list is None:
            raise ValueError("No command file or list specified.")

        # Using list of command strings

        # Ensure command_list is a list of strings
        for cmd in command_list:
            if type(cmd) is not str:
                raise TypeError("command_list must be a list of strings")

        mode = "list"
    else:
        # Using file containing commands
        mode = "file"

    # Connect to the Minecraft server via RCON
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        if mode == "file":
            # Open the file with the Minecraft commands
            with open(COMMAND_FILE_PATH, 'r') as command_file:
                for line in command_file:
                    # remove any trailing whitespace or newline
                    command = line.strip()
                    if command:
                        # remove leading '/'
                        if command[0] == '/':
                            command = command[1:]

                        # set vanilla cmd prefix if needed
                        cmd_prefix = "" if not USE_VANILLA_PREFIX else "minecraft:"

                        # add the cmd prefix
                        command = f"{cmd_prefix}{command}"

                        # send the command to the server
                        mcr.command(command)
                        print(f"Executed: {command}\nServer Response: ", end="")
        elif mode == "list":
            for command in command_list:
                # remove any trailing whitespace or newline
                command = command.strip()
                if command:
                    # remove leading '/'
                    if command[0] == '/':
                        command = command[1:]

                    # set vanilla cmd prefix if needed
                    cmd_prefix = "" if not USE_VANILLA_PREFIX else "minecraft:"

                    # add the cmd prefix
                    command = f"{cmd_prefix}{command}"

                    # send the command to the server
                    mcr.command(command)
                    print(f"Executed: {command}\nServer Response: ", end="")

def send_cmd_str(command: str, cmd_prefix: str = None):
    """
    Sends a single command to the Minecraft server.
    :param command: command to send. Must be a string.
    :param cmd_prefix: prefix string to use for command. Must be a string or None.
    Example: "minecraft:" or "forge:"
    :return: the server's response if any (as a string)
    """
    # remove leading '/'
    if command[0] == '/':
        command = command[1:]

    # set vanilla cmd prefix
    if cmd_prefix is None and USE_VANILLA_PREFIX:
        cmd_prefix = "minecraft:"
    elif cmd_prefix is None:
        cmd_prefix = ""

    # add the cmd prefix
    command = f"{cmd_prefix}{command}"

    # Connect to the Minecraft server via RCON
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        cmd = command.strip()  # Remove any trailing whitespace or newline
        if cmd:
            response = mcr.command(cmd)  # Send the command to the server
            print(f"\nExecuted:\n{cmd}\n\nServer Response: ")
            return response
    return None

if __name__ == '__main__':
    # Run the function
    source_file = "commands.txt"
    if len(argv) < 2:
        print("No source file given. Defaulting to 'commands.txt'")
    else:
        source_file = argv[1]
    send_commands_to_minecraft(source_file)
