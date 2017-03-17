import random


def process(user_input, nlu_data):
    try:
        greeting_text = ['Hi!',
        'Hello!',
        'Howdy',
        'hello user',
        'How many times are you going to say hello?',
        'Hi there! I\'m the Banker, your banking assistant'
        ]

        out_text = random.choice(greeting_text)

        output = {
        'bot_response_text': out_text,
        'context': 'None'
        }
        return output
    except Exception as e:
        print e
        output = {
        'bot_response_text': e,
        'context': 'None'
        }
