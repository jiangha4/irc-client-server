

def handle_message(user, prefix, cmd, cmd_args, server):
    print("Got new message")
    print(cmd_args)
    command_handler[cmd](user, prefix, cmd, cmd_args, server)

def nick(user, prefix, cmd, cmd_args, server):
    input_nick = cmd_args[0]
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

def user(user, prefix, cmd, cmd_args, server):
    print("USER")
    username = cmd_args[0]
    user.set_username(username)
    user.register()

def join():
    pass

def quit():
    pass

command_handler = {
    "NICK": nick,
    "USER": user,
    "JOIN": join,
    "QUIT": quit
}