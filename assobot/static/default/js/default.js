const plugin_switch = document.getElementsByClassName('plugin-switch');

function update_plugin_enable_state(plugin_id, is_enabled) {
    route_end_point = is_enabled ? '/enabled' : '/disabled'
    axios.get('/plugin/' + plugin_id + route_end_point)
         .catch(function (error) {
             console.log(error);
         })
}


for (const element of plugin_switch) {
    element.addEventListener('click', function () {
        update_plugin_enable_state(element.name, element.checked)
    })
}