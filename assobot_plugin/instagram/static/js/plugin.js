function remove_profile() {
    reaction_list = document.getElementById("profiles-list")
    if (reaction_list.children.length > 1)
        reaction_list.removeChild(reaction_list.lastChild);
}

function add_profile() {
    reaction_list = document.getElementById("profiles-list")
    let clone = reaction_list.children[0].cloneNode(true)
    reaction_list.appendChild(clone)
}