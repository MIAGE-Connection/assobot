from urllib import parse

TOKEN="OTU3OTM4OTU1OTE4MTM1MzQ2.YkGELA.M1CLMonwQZ6ZBZIzYgrflpmrEBk"
CLIENT_SECRET="M8v2APwEsqslYc78EsawJT5cTjTItrWa"
REDIRECT_URL="http://127.0.0.1:5000/oauth/callback"
REDIRECT_OAUTH_URL=f"https://discord.com/api/oauth2/authorize?client_id=957938955918135346&redirect_uri={parse.quote(REDIRECT_URL)}&response_type=code&scope=identify%20email%20guilds%20guilds.join%20guilds.members.read"