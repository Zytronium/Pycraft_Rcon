# Pycraft Rcon

This project contains python commands that interact with a running minecraft
server with RCON enabled. It sends a series of minecraft commands to the server
via RCON. You can import and run the python functions in pycraftCommands.py, you
can send an exact command string to the server with `send_cmd_str()`, or you can
send a series of commands to the server with `send_commands_to_minecraft()`.
Your server needs to have rcon enabled, and you need to specify the rcon
hostname, rcon port, and rcon password in the "connection_settings" file that
will appear after running for the first time.

## Tips
The recommended place to write your script to interact with the server is in main.py.
You can find preset functions in presets.py.

Running commands on threads will not currently work due to the way sending
commands to rcon is set up. If you wish to do something like this, to run
multiple minigame presets at the same time for example, you may create another
Python script which imports all presets with this line: `from presets import *`.
You can then run more than one preset at the same time by running both python
scripts separately.

The commands used in this project were designed to be used in Minecraft version
1.21.3. While I will try to keep it working on whatever the latest version is
as new updates release, I cannot guarantee that commands will ALWAYS work as
intended on any other version, nor can I guarantee that I will come back to this
project in order to make it work on newer versions.

## Required modules to run
- Mcron
  - how to install:
    ```bash
    pip install mcrcon
    ```

## Minecraft server setup
If you are wanting to try this, you might already have a minecraft server set up.
However, if you do not, or at least don't have rcon set up, here's how.
Note: this is for Java Editions servers only.

Skip to "Rcon Setup" or "Pycraft Rcon Connection Settings Setup" if you already
have a minecraft server set up.

#### Minecraft Server Download (for a locally hosted server)
Download a minecraft server jar file from the Minecraft launcher. To find the
download link, make sure you are in the **Java Edition** page in the launcher
(found on the left side of the window), then go to the "**Installations**" tab
(found at the top of the window). Click on the "**New Installation**" button
(just below the search bar at the top of the window), ***or*** edit an existing
installation of the version you want your server on, by clicking on the **3
vertical dots** on the right side of the installation listed and selecting
"**Edit.**" Make sure the Minecraft version you want is selected under
**"Version"**, then, to the right of the "Version" label, click the
"**Server**" button with the download icon next to it. This will download
a `server.jar` file.

#### Initial Server Setup
Move the `server.jar` file to its own folder, which will contain all the
server's files. Run the jar; it will create a few initial files, including
`eula.txt`. Open that text file and agree to the EULA by changing "false" to
"true" and save the file. Running the server after this should now work. You can
connect to the server in minecraft with the IP `localhost`, your IPv4 address, 
or "0.0.0.0:`port`" (where `port` is your server's port, 25565 by default).

If you want people to be able to connect to your server externally, you have to
specify the IP address in the `server.properties` file, ensure online mode is
true, and port forward to allow connecting to your server from other Wi-Fi
networks. This may be a security risk, and how you do this varies based on your
router and/or ISP. Connecting from another machine on the same network does not
require port forwarding, but may require that you specify your IPv4 address as
the server IP in the properties file. You can connect to your server from the
computer running it, in the "Server Address" field in Minecraft, input
"`localhost`", your IPv4 address, or your public IP address (or "0.0.0.0" if you
left the server ip blank in `server.properties`) followed by the port specified
in the `server.properties` file (25565 by default). To connect to it from
another Wi-Fi network, input your public IP address followed by the port,
like this: `your.public.ip:port` (example: `12.345.67.890:25565`).

Note: if you cannot run the jar due to a Java/jvm error, you may need a
newer version of Java installed.

### Rcon Setup
Open the `server.properties` file and change the value for `enable-rcon` from
"false" to "true." Then, set a **secure** rcon password as the value for
`rcon.password`. Change the `rcon.port` value *if needed*, but the default value
of 25575 should work. If you don't want OPed players like yourself to see in
chat all the commands rcon is executing, change `broadcast-rcon-to-ops` to
false. Save the file, restart your server to apply the changes if it was running.

### Pycraft Rcon Connection Settings Setup
Run `main.py` or `pycraftCommands.py`. This will create the
`connection_settings` text file. Open that file and change the values according
to your server setup.

##### Rcon Host
The `rcon host` option should be the server address, which
could be "localhost", your IPv4 address, your public IP address
(without the port), or "0.0.0.0" (if you don't have an IP set in the
server properties) if running locally, or just the server's public IP address
if it's being hosted on another network and you've port forwarded both ports.

##### Rcon Port
The `rcon port` option should be the `rcon.port` value in the
`server.properties` file. Be default, this is 25575. Again, if you are hosting
from another network, you must not only port forward the server's IP + port,
but also the server's IP + *rcon* port in order for rcon to work. 

##### Rcon Password
The `rcon password` option should be the value of `rcon.password` in the
`server.properties` file. 

Note: do not leave any text anywhere else in this file. It may cause the
program to be unable to properly read the file. Even an extra blank line at
the end can cause issues. This is a bug.
