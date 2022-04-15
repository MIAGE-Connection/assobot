def parse_welcome_message(msg, member, channel):

    TOKENS = {
        "[[MEMBER]]" : member.mention,
        "[[GUILD]]" : member.guild.name,
        "[[CHANNEL]]" : channel.name
    }

    for key in TOKENS.keys():
        if key in msg:
            msg = msg.replace(key, TOKENS[key])
    
    return msg