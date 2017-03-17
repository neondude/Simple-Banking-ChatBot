import config
import json
import urllib
import requests
import sys
from src import *

API_AI_CLIENT_KEY = config.API_AI_CLIENT_KEY


def process_query(user_input,sessionid):
    try:
        r = requests.get('https://api.api.ai/v1/query?v=20170310&'+ 'query=' + urllib.quote_plus(user_input['user_input_text'])+'&lang=en&sessionId='+sessionid ,
                         headers={
                             'Authorization': 'Bearer %s' % API_AI_CLIENT_KEY
                             }
                         )
        data = r.json()
        if data['result']['action'] == 'input.unknown' and user_input['context'] == 'None':
            output = {
                'bot_response_text': "Sorry i did not understand that. Can you ask me a bit more clearly?" ,
                'context': 'None'
            }
            return output
        nlu_data = {
            'intent' : data['result']['metadata']['intentName'],
            'parameters' : data['result']['parameters']
        }
        if user_input['context'] != "None":
            bot_module = user_input['context']
        else:
            bot_module = nlu_data['intent']

        bot_output = sys.modules['modules.src.' + bot_module].process(user_input, nlu_data)
        return bot_output
    except  Exception as e:
        print
        print
        print e
        print
        print
        output = {
            'bot_response_text': e ,
            'context': 'None'
        }
        return output

def test_query(user_input,sessionid):
    r = requests.get('https://api.api.ai/v1/query?v=20170310&'+ 'query=' + 'help'+'&lang=en&sessionId='+sessionid ,
                     headers={
                         'Authorization': 'Bearer %s' % API_AI_CLIENT_KEY
                         }
                     )
    data = r.json()
    nlu_data = {
        'intent' : data['result']['metadata']['intentName'],
        'parameters' : data['result']['parameters']
    }
    print nlu_data
    bot_output = sys.modules['modules.src.' + nlu_data['intent']].process(user_input, nlu_data)
    return bot_output
    return output


# def search(input, sender=None, postback=False):
#     if postback:
#         payload = json.loads(input)
#         intent = payload['intent']
#         entities = payload['entities']
#     else:
#         intent, entities = process_query(input)
#     if intent is not None:
#         if intent in src.__personalized__ and sender is not None:
#             r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
#                 'fields': 'first_name',
#                 'access_token' : os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
#             })
#             entities['sender'] = r.json()
#         data = sys.modules['modules.src.' + intent].process(input, entities)
#         if data['success']:
#             return data['output']
#         else:
#             if 'error_msg' in data:
#                 return data['error_msg']
#             else:
#                 return TextTemplate('Something didn\'t work as expected! I\'ll report this to my master.').get_message()
#     else:
#         return TextTemplate('I\'m sorry; I\'m not sure I understand what you\'re trying to say sir.\nTry typing "help" or "request"').get_message()
