# IRC-Client-Server

### Purpose
This repository contains a python3 implementation of an IRC Server and Client built 
according to RFC specifications. The server is dockerized and listens on port 8888.

### Server
The server container can be built with:
```bash
docker build -t irc-server .
```

Then, you can start the server with:
```bash
docker run -p 8888:8888 -t irc-server
```

### Client
To connect to the server, run:
```bash
python client/client.py -n $nickname -u $username -f $fullname
```
Nickname, username, and fullname must be supplied at invocation. 

Current support commands:
1. QUIT - Quit the server
2. NICK - Change or set nickname
3. JOIN - Join a channel
4. PRIVMSG - Send a private message to another user
5. PART - Leave a channel
6. LIST - List all channels
7. NAMES - List of users
8. TOPIC - Send a message to a channel or create it if it doesn't exist