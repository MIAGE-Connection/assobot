from urllib import parse

REDIRECT_URL='http://127.0.0.1:5000/oauth/callback'
REDIRECT_URL_GUILD='http://127.0.0.1:5000/guild/callback'
REDIRECT_OAUTH_URL=f"https://discord.com/api/oauth2/authorize?client_id=957938099609022514&redirect_uri={parse.quote(REDIRECT_URL)}&response_type=code&prompt=none&scope=identify%20email%20connections%20guilds%20guilds.members.read"
PARTIAL_URL_BOT_ADD=f"https://discord.com/api/oauth2/authorize?client_id=957938099609022514&permissions=8&redirect_uri={parse.quote(REDIRECT_URL_GUILD)}&response_type=code&scope=bot&disable_guild_select=true&guild_id="