import os
from flask import *
from pathlib import Path
from zenora import APIClient
from werkzeug.utils import secure_filename
from assobot import APP, ASSOBOT_PLUGIN_TEMP_FOLDER, BOT, GUILD_MANAGER, PARTIAL_URL_BOT_ADD, AUTH_MANAGER, PLUGIN_FACTORY

@APP.route('/guilds')
@APP.route('/guilds/')
def guild_list():
    if not 'token' in session: return abort(403, description="Unauthorized action")
    
    bearer_client = APIClient(session.get('token'), bearer=True)

    guilds_joined = list()
    guilds_not_joined = list()

    for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                GUILD_MANAGER.add(guild)
                if GUILD_MANAGER.get(guild.id).is_bot_member():
                    guilds_joined.append(guild)
                else:
                    guilds_not_joined.append(guild)
    return render_template('default/guilds.html', guilds_joined=guilds_joined, guilds_not_joined=guilds_not_joined, partial_url=PARTIAL_URL_BOT_ADD)

@APP.route('/guilds/<guild_id>', methods=['GET', 'POST'])
def guild_manage(guild_id):
    if 'token' in session and guild_id:
        ctx = AUTH_MANAGER.get_current_ctx()
        ctx.guild = GUILD_MANAGER.get(int(guild_id))
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']

            if file.filename == '':
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                dst_file_path = Path(os.path.join(ASSOBOT_PLUGIN_TEMP_FOLDER, filename))
                file.save(dst_file_path)
                plugin = PLUGIN_FACTORY.install_plugin(dst_file_path)
                ctx.guild.add_plugin(plugin)
        return render_template('default/plugin/plugin_list.html', guild=ctx.guild)
    else:
        return abort(403, description="Unauthorized action")



@APP.route('/guild/callback')
def callback_guild():
    guild_id = request.args['guild_id']
    return redirect(f"/guilds/{guild_id}")
