Specify in the `settings` file which file in this folder to use. Each file should
be formatted like `default` preset in this folder. If you mess up the default preset
and cannot correct it, delete it and rerun the program to regenerate the file.
Any additional unexpected text, besides the values for the below settings, will
cause an error while reading the file. Even blank lines can cause this. This is a bug.
a
## Connection Settings Explanation
- `rcon host: localhost`
  - replace `localhost` with the server's IP address. Depending on the scenario, this can be any of the following:
    - `localhost`
    - `0.0.0.0`
    - Your IPv4 address
    - The server's public IP address
- `rcon port: 25575`
  - replace `25575` with the server's **rcon** port specified in the server's `server.properties` file. By default, this is `25575`.
- `rcon password: change_me`
  - replace `change_me` with the server's rcon password you specified in the server's `server.properties` file. By default, this is blank. Rcon will not start if it is still blank.
- `require vanilla cmd prefix: false`
  - replace `false` with `true` if your server requires the "minecraft:" prefix to run vanilla minecraft commands. (i.e. if you have certain server plugins) 
- `compatible nuke cmd: false`
  - replace `false` with the required command in order to nuke. The command's syntax must be compatible with this program's code that sends this command.
    - i.e. "compatible nuke cmd: send_nuke"
      - assuming the command syntax is something like: `/send_nuke <player name or entity UUID> <missile mode (true/false)>`
  - leaving as `false` will use vanilla minecraft commands to create a nuke.