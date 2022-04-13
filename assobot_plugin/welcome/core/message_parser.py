def parse_welcome_message(msg, member):

    TOKENS = {
        "{% MEMBER %}" : member.mention,
        "{% GUILD %}" : member.guild,
        "{% CHANNEL %}" : member.guild.system_channel
    }

    for key in TOKENS.keys():
        if key in msg:
            msg = msg.replace(key, TOKENS[key])
    
    return msg