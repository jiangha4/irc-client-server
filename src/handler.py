

def handle_message(user, message, server):
    cmd = message.command
    command_handler[cmd](user, message, server)


def nick(user, message, server):
    print(message)
    input_nick = message.command_params[0]
    usr = server.get_user(input_nick)
    if usr:
        if (usr.nickname == input_nick) and usr.alive:
            # send ERR_NICKNAMEINUSE
            pass
        else:
            usr.set_nickname(input_nick)
    else:
        #user not found
        user.set_nickname(input_nick)

def user(user, message, server):
    print("USER")

def join():
    pass

def quit():
    pass

command_handler = {
    "NICK": nick,
    "USER": user,
    "JOIN": join,
    "QUIT": quit}