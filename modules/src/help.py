def process(user_input, nlu_data):
    #out_text = 'Hi there! I\'m the Banker, your banking assistant'
    out_text = 'Here are some of the things i can do'
    out_text += '<br>  - help you withdraw money from your account'
    out_text += '<br>  - help you deposit money from your account'
    out_text += '<br>  - tell you your account balance'
    out_text += '<br>  - tell your account summary'
    #out_text += '<br>Have a nice day. :)'

    output = {
        'bot_response_text': out_text,
        'context': 'None'
    }
    return output
