nova <user.text>$:
    result = user.command_match(text, user.SimpleCommandGetter)
    user.nova_hide()
    user.nova_show(result)

nova close: 
    user.nova_hide()

