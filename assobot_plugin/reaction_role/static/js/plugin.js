function remove_reaction() {
    reaction_list = document.getElementById("reaction-role-list")
    if (reaction_list.children.length > 1)
        reaction_list.removeChild(reaction_list.lastChild);
}

function add_reaction() {
    reaction_list = document.getElementById("reaction-role-list")
    let clone = reaction_list.children[0].cloneNode(true)
    reaction_list.appendChild(clone)
}