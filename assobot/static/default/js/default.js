const plugin_switch = document.getElementsByClassName('plugin-switch');

function update_plugin_enable_state(guild_id, plugin_id, is_enabled) {
    route_end_point = is_enabled ? '/enabled' : '/disabled'
    url = '/guilds/' + guild_id + '/plugins/' + plugin_id + route_end_point
    axios.get(url)
        .catch(function (error) {
            console.log(error);
        }).then(function (result) {
            console.log(result);
        })
}


for (const element of plugin_switch) {
    element.addEventListener('click', function () {
        let guild_id = element.name.split('~')[0]
        let plugin_id = element.name.split('~')[1]
        update_plugin_enable_state(guild_id, plugin_id, element.checked)
    })
}