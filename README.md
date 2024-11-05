# Pycraft Rcon

This project contains python commands that interact with a running minecraft
server with RCON enabled. It sends a series of minecraft commands to the server
via RCON. You can import and run the python functions in pycraftCommands.py, you
can send an exact command string to the server with `send_cmd_str()`, or you can
send a series of commands to the server with `send_commands_to_minecraft()`.
Your server needs to have rcon enabled, and you need to specify the rcon
hostname, rcon port, and rcon password in the "connection_settings" file that
will appear after running for the first time.

The recommended place to write your script to interact with the server is in main.py.
You can find preset functions in presets.py. 
