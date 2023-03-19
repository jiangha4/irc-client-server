"""This module contains the message handlers"""

import logging
from itertools import zip_longest
from message import IRCReply
from channel import Channel

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def send_to_user(user, server, text, cmd):
    if user.alive:
        msg_obj = IRCReply(server.get_prefix(), cmd, text)
        user.send(msg_obj.get_message())


def handle_message(user, server, message):
    logger.info("Command: {}".format(message.get_command()))
    logging.info(message.get_command_params())

    cmd = message.get_command()

    if cmd not in command_handler:
        if user.is_registered():
            # Returned to a registered client to indicate that the
            # command sent is unknown by the server.
            text = ":Unknown command"
            cmd = "ERR_UNKNOWNCOMMAND"
            send_to_user(user, server, text, cmd)
    else:
        # else, if command is known, handle command
        if user.is_registered() or cmd == "USER" or cmd == "NICK":
            command_handler[cmd](user, server, message)
        else:
            text = ":You have not registered"
            cmd = "ERR_NOTREGISTERED"
            send_to_user(user, server, text, cmd)


def nick(user, server, message):
    try:
        old_nick = user.get_nickname()
        input_nick = message.get_command_params()[0]

        if server.is_nick_registered(input_nick):
            # send ERR_NICKNAMEINUSE if nickname is used by other registered user
            text = "<{}> :Nickname is already in use".format(input_nick)
            cmd = "ERR_NICKNAMEINUSE"
            send_to_user(user, server, text, cmd)
        else:
            # Set user name or update
            user.set_nickname(input_nick)

            # Check to see if this user has created any channels, and if they have
            # Update channel creator to new nick
            for channel in server.get_all_channels():
                if channel.get_creator() == old_nick:
                    channel.set_creator(input_nick)

    except IndexError:
        # Return ERR_NONICKNAMEGIVEN if nickname parameter is not found
        text = ":No nickname given"
        cmd = "ERR_NONICKNAMEGIVEN"
        send_to_user(user, server, text, cmd)


def user(user, server, message):
    # User message format: <user> <mode> <unused> <realname>
    # Check for enough command params
    message_params = message.get_command_params()
    if len(message_params) < 4:
        text = "<USER> :Not enough parameters"
        cmd = "ERR_NEEDMOREPARAMS"
        send_to_user(user, server, text, cmd)
        return

    # Check for already registered user
    if user.is_registered():
        text = ":Unauthorized command (already registered)"
        cmd = "ERR_ALREADYREGISTRED"
        send_to_user(user, server, text, cmd)
        return

    username = message.get_command_params()[0]
    mode = message.get_command_params()[1]
    # Remove initial :
    fullname = message.get_command_params()[3][1:]
    user.register(mode, username, fullname)

    if user.is_registered():
        text = "Welcome to the Internet Relay Network {}!{}@{}".format(
            user.get_nickname(), user.get_username(), user.get_hostname()
        )
        cmd = "RPL_WELCOME"
    else:
        text = ":You have not registered"
        cmd = "ERR_NOTREGISTERED"

    send_to_user(user, server, text, cmd)


def join(user, server, message):
    try:
        channels = message.get_command_params()[0].split(",")
        if channels == "0":
            all_channels = server.get_all_channels()
            for channel in all_channels:
                if channel.is_user_in_channel(user.get_nickname()):
                    channel.remove_user(user.get_nickname())
            return
        # Try and parse passwords. If no passwords, skip
        try:
            passwords = message.get_command_params()[1].split(",")
        except IndexError:
            passwords = []

        for name, pswd in zip_longest(channels, passwords, fillvalue=None):
            cname = name[1:]
            ch = server.get_channel(cname)
            if ch:
                # if the channel exists, check the password
                # add the user to the channel if the password matches
                # or if the password is None
                if ch.get_password() == pswd or not ch.get_password:
                    text = "JOIN {}".format(name)
                    prefix = "{}!{}@{}".format(
                        user.get_nickname(),
                        user.get_username(),
                        user.get_hostname(),
                    )
                    for usr in ch.get_users():
                        msg = prefix + " " + text + "\r\n"
                        usr.send(msg)

                    if not ch.is_user_in_channel(user.get_nickname()):
                        ch.add_user(user)
                    # Check if channel has a topic
                    topic = ch.get_topic()
                    if topic:
                        text = "<{}> :<{}>".format(cname, topic)
                        cmd = "RPL_TOPIC"
                    else:
                        text = "<{}> :No topic is set".format(cname)
                        cmd = "RPL_NOTOPIC"
                else:
                    text = ":Password incorrect"
                    cmd = "ERR_PASSWDMISMATCH"
            else:
                new_channel = Channel(cname, user.get_nickname(), pswd)
                new_channel.add_user(user)
                server.add_channel(new_channel)
                text = "<{}> :No topic is set".format(cname)
                cmd = "RPL_NOTOPIC"
            send_to_user(user, server, text, cmd)
        return
    except IndexError:
        text = "<JOIN> :Not enough parameters"
        cmd = "ERR_NEEDMOREPARAMS"

    send_to_user(user, server, text, cmd)


# todo: if message exists, send to others in channels
# todo: remove user from channels
def quit(user, server, message):
    logger.info("Command QUIT")
    user.quit()


def private(user, server, message):
    msg_params = message.get_command_params()
    # If there are not 2 parts to the message, the message is incorrectly formatted
    # todo: revisit this error checking
    if len(msg_params) < 2:
        try:
            if msg_params[0].startswith(":"):
                text = ":No recipient given (PRIVMSG)"
                cmd = "ERR_NORECIPIENT"
            else:
                text = ":No text to send"
                cmd = "ERR_NOTEXTTOSEND"
            send_to_user(user, server, text, cmd)
        except IndexError:
            text = "<PRIVMSG> :Not enough parameters"
            cmd = "ERR_NEEDMOREPARAMS"
            send_to_user(user, server, text, cmd)
        return
    else:
        # check if message is directed to channels or users
        targets = msg_params[0]
        for target in targets.split(","):
            if target.startswith("#"):
                cname = target[1:]
                # send to channels
                if server.does_channel_exist(cname):
                    channel = server.get_channel(cname)
                    # get users in channel
                    for usr in channel.get_users():
                        # Don't send a message to yourself
                        if usr.get_nickname() != user.get_nickname():
                            prefix = "{}!{}@{}".format(
                                user.get_nickname(),
                                user.get_username(),
                                user.get_hostname(),
                            )
                            msg_text = msg_params[1]
                            msg = "{} PRIVMSG {} {}".format(
                                prefix, target, msg_text
                            )
                            usr.send(msg)
                else:
                    text = "<{}> :No such nick".format(cname)
                    cmd = "ERR_NOSUCHNICK"
                    send_to_user(user, server, text, cmd)
            else:
                # send to users
                target_usr = server.get_user(target)
                if target_usr and target_usr.alive:
                    prefix = "{}!{}@{}".format(
                        user.get_nickname(),
                        user.get_username(),
                        user.get_hostname(),
                    )
                    msg_text = msg_params[1]
                    msg = "{} PRIVMSG {}".format(prefix, msg_text)
                    target_usr.send(msg)
                else:
                    text = "<{}> :No such nick".format(target)
                    cmd = "ERR_NOSUCHNICK"
                    send_to_user(user, server, text, cmd)
            return


def list(user, server, message):
    message_params = message.get_command_params()
    if len(message_params) == 0:
        # list all public channels
        channels = server.get_public_channels()
        # find private channels that the user is a part of and add them
        # to channels list
        private_channels = server.get_private_channels()
        for private_channel in private_channels:
            if private_channel.is_user_in_channel(user.get_nickname()):
                channels.append(private_channel)
    else:
        channel_names = message.get_command_params()[0].split(",")
        channels = []
        for channel_name in channel_names:
            cname = channel_name[1:]
            if server.does_channel_exist(cname):
                ch = server.get_channel(cname)
                # Only include channel if the user is in the specified channel
                if ch.is_user_in_channel(user.get_nickname()):
                    channels.append(server.get_channel(cname))
                else:
                    text = "<{}> :You're not on that channel".format(cname)
                    cmd = "ERR_NOTONCHANNEL"
                    send_to_user(user, server, text, cmd)
            else:
                text = "<{}> :No such channel".format(cname)
                cmd = "ERR_NOSUCHCHANNEL"
                send_to_user(user, server, text, cmd)

    for channel in channels:
        name = channel.get_name()
        topic = channel.get_topic()
        if not topic:
            topic = "No topic is set"
        text = "<{}> :{}".format(name, topic)
        cmd = "RPL_LIST"
        send_to_user(user, server, text, cmd)

    text = ":End of LIST"
    cmd = "RPL_LISTEND"
    send_to_user(user, server, text, cmd)


def names(user, server, message):
    message_params = message.get_command_params()
    if len(message_params) == 0:
        # list all channels
        channels = server.get_public_channels()
        private_channels = server.get_private_channels()
        for private_channel in private_channels:
            if private_channel.is_user_in_channel(user.get_nickname()):
                channels.append(private_channel)
    else:
        channel_names = message.get_command_params()[0].split(",")
        channels = []
        for channel_name in channel_names:
            cname = channel_name[1:]
            if server.does_channel_exist(cname):
                ch = server.get_channel(cname)
                if ch.is_user_in_channel(user.get_nickname()):
                    channels.append(server.get_channel(cname))
                else:
                    text = "<{}> :You're not on that channel".format(cname)
                    cmd = "ERR_NOTONCHANNEL"
                    send_to_user(user, server, text, cmd)
            else:
                text = "<{}> :No such channel".format(cname)
                cmd = "ERR_NOSUCHCHANNEL"
                send_to_user(user, server, text, cmd)

    for channel in channels:
        cname = channel.get_name()
        users = channel.get_users()
        user_str = ""
        for usr in users:
            template = "@{} "
            user_str = user_str + template.format(usr.get_nickname())

        text = "<{}> :{}".format(cname, user_str)
        cmd = "RPL_NAMREPLY"
        send_to_user(user, server, text, cmd)

        text = "<{}> :End of NAMES list".format(cname)
        cmd = "RPL_ENDOFNAMES"
        send_to_user(user, server, text, cmd)


def part(user, server, message):
    msg_parts = message.get_command_params()
    if not msg_parts:
        text = "<PART> :Not enough parameters"
        cmd = "ERR_NEEDMOREPARAMS"
        send_to_user(user, server, text, cmd)
        return

    channel_names = msg_parts[0].split(",")
    for channel_name in channel_names:
        cname = channel_name[1:]
        if server.does_channel_exist(cname):
            channel = server.get_channel(cname)
            nickname = user.get_nickname()
            if channel.is_user_in_channel(nickname):
                channel.remove_user(nickname)

                # if there is a message, send it
                try:
                    parting_msg = msg_parts[1]
                    for usr in channel.get_users():
                        # Don't send a message to yourself
                        if usr.get_nickname() != user.get_nickname():
                            prefix = "{}!{}@{}".format(
                                user.get_nickname(),
                                user.get_username(),
                                user.get_hostname(),
                            )
                            msg = "{} PRIVMSG {} {}".format(
                                prefix, cname, parting_msg
                            )
                            usr.send(msg)
                except IndexError:
                    pass

            else:
                text = "<{}> :You're not on that channel".format(cname)
                cmd = "ERR_NOTONCHANNEL"
                send_to_user(user, server, text, cmd)

        else:
            text = "<{}> :No such channel".format(cname)
            cmd = "ERR_NOSUCHCHANNEL"
            send_to_user(user, server, text, cmd)


def topic(user, server, message):
    msg_parts = message.get_command_params()
    if not msg_parts:
        text = "<TOPIC> :Not enough parameters"
        cmd = "ERR_NEEDMOREPARAMS"
        send_to_user(user, server, text, cmd)
        return

    channel_name = msg_parts[0]
    if not channel_name.startswith("#"):
        text = "<{}> :Bad Channel Mask".format(channel_name)
        cmd = "ERR_BADCHANMASK"
        send_to_user(user, server, text, cmd)
        return

    cname = channel_name[1:]
    channel = server.get_channel(cname)

    if not server.does_channel_exist(cname):
        text = "<{}> :No such channel".format(cname)
        cmd = "ERR_NOSUCHCHANNEL"
        send_to_user(user, server, text, cmd)
        return

    if channel.get_creator() != user.get_nickname():
        text = "<{}> :You're not channel operator".format(cname)
        cmd = "ERR_CHANOPRIVSNEEDED"
        send_to_user(user, server, text, cmd)
        return

    try:
        topic_msg = msg_parts[1]
        channel.set_topic(topic_msg[1:])
    except IndexError:
        channel.clear_topic()

    ch_topic = channel.get_topic()
    if ch_topic:
        text = "<{}> :<{}>".format(cname, ch_topic)
        cmd = "RPL_TOPIC"
    else:
        text = "<{}> :No topic is set".format(cname)
        cmd = "RPL_NOTOPIC"
    send_to_user(user, server, text, cmd)


command_handler = {
    "NICK": nick,
    "USER": user,
    "JOIN": join,
    "QUIT": quit,
    "PRIVMSG": private,
    "LIST": list,
    "NAMES": names,
    "PART": part,
    "TOPIC": topic,
}
