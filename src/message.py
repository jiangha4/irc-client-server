WHITESPACE_CHAR = " "


class BadMessageException(Exception):
    pass


class IRCReply(object):
    """Server replies to clients"""

    command_dict = {
        "RPL_WELCOME": "001",
        "RPL_LIST": "322",
        "RPL_LISTEND": "323",
        "RPL_NOTOPIC": "331",
        "RPL_TOPIC": "332",
        "RPL_NAMREPLY": "353",
        "RPL_ENDOFNAMES": "366",
        "ERR_NOSUCHNICK": "401",
        "ERR_NOSUCHCHANNEL": "403",
        "ERR_NORECIPIENT": "411",
        "ERR_NOTEXTTOSEND": "412",
        "ERR_UNKNOWNCOMMAND": "421",
        "ERR_NICKNAMEINUSE": "433",
        "ERR_NOTONCHANNEL": "442",
        "ERR_NOTREGISTERED": "451",
        "ERR_NEEDMOREPARAMS": "461",
        "ERR_PASSWDMISMATCH": "464",
        "ERR_ALREADYREGISTRED": "462",
        "ERR_BADCHANMASK": "476",
        "ERR_CHANOPRIVSNEEDED": "482",
    }

    def __init__(self, prefix, command, command_params):
        self.prefix = prefix
        self.command = self.command_dict[command]
        self.command_params = command_params
        self.message = self.generate_message()

    def generate_message(self):
        template = ":{prefix} {command} {params} \r\n"
        message = template.format(
            prefix=self.prefix,
            command=self.command,
            params=self.command_params,
        )
        return message

    def get_message(self):
        return self.message


class IRCClientMessage(object):
    """Standard IRC message from a client"""

    def __init__(self, command, *command_params):
        self.command = command
        self.command_params = [command]
        for param in command_params:
            self.command_params.append(param)
        self.message = self.generate_message()

    def generate_message(self):
        return WHITESPACE_CHAR.join(self.command_params) + "\r\n"

    def get_message(self):
        return str(self.message)


class IRCMessage(object):
    """
    Standard IRC message from either a client
    Built using RFC 2812 as a reference
    """

    # Clients do not prefix
    # Prefixs are used by the server to indicate the true origin of the message
    def __init__(self, prefix, command, command_params):
        self.prefix = prefix
        self.command = command
        self.command_parameters = command_params

    def get_prefix(self):
        return self.prefix

    def get_command(self):
        return self.command

    def get_command_params(self):
        return self.command_parameters


def parse_message(raw_message):
    print(raw_message)
    prefix = None
    command = None
    command_parameters = []

    # RFC 2812 - IRC messages are always lines of characters terminated with a CR-LF
    if raw_message[-2:] != "\r\n":
        raise BadMessageException()

    # Remove termination characters from string to handle easier
    message = raw_message[:-2]
    # Check if message is still valid and does not just contain \r\n
    # RFC 2812 - Empty messages are silently ignored, which permits use of the sequence CR-LF
    # between messages without extra problems
    if len(message) <= 0:
        return

    # RFC 2812 - The prefix, command, and all parameters are separated by one ASCII space character
    parts = message.split(" ")
    # Check for prefix
    if parts[0][0] == ":":
        prefix = parts[0]
        command = parts[1]
        index = 2
    else:
        command = parts[0]
        index = 1

    try:
        for i in range(index, len(parts)):
            # If command parameters start with ':', we know the rest of parsed message part of the
            # command parameters
            if parts[i][0] == ":":
                command_parameters.append(WHITESPACE_CHAR.join(parts[i:]))
                break
            else:
                # command parameters before the message
                command_parameters.append(parts[i])
    except IndexError:
        command_parameters = []

    return IRCMessage(prefix, command, command_parameters)
