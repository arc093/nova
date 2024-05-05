nova <user.text>$:
    result = user.gpt_answer_question(text)
    user.nova_hide()
    user.nova_show(result)

nova close: 
    user.nova_hide()