# IRC-Client-Server
![workflow](https://github.com/jiangha4/irc-client-server/workflows/IRC-Server-Module/badge.svg)

## Purpose
This repository contains a python3 implementation of an IRC Server and Client built 
according to RFC specifications. The server is dockerized and listens on port 8888.

## Usage

### Server
To run the server:
```bash
docker-compose up
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

## Contributions
All server source code is contained with `src/server/` and client interface is contained in
`client/`.

From the root directory:

Tests and linting:
```bash
tox
```

Generated test reports are located in `reports/`.

Pylint rc file located `utils/pylint.rc`.

To run the Black formatter:
```bash
tox -e format
```

Formatter is run separately to allow for CI/CD purposes. Allows automated CD to run tox unittests and
linting check without running a Black formatting pass. 

### Github Actions Workflow
Github actions workflow is located in `.github/workflows`. Runs a tox build on push and pull requests. 
Status badge is displayed on this README. 