import random


def process(user_input, nlu_data):
    try:
        fallback_text = ['sorry, i didn\'t get that. Could you ask a bit more clearly!'
        ]

        out_text = random.choice(fallback_text)

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
