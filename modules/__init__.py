import config
import json
import requests
import sys
from src import * 

API_AI_CLIENT_KEY = config.API_AI_CLIENT_KEY


def process_query(user_input,sessionid):
    try:
        r = requests.get('https://api.api.ai/v1/query?v=20170310&'+ 'query=' + user_input+'&lang=en&sessionId='+sessionid ,
                         headers={
                             'Authorization': 'Bearer %s' % API_AI_CLIENT_KEY
                             }
                         )
        data = r.json()
        return data
    except  Exception as e:
        return e


if __name__ == '__main__':
    process_query("hello" ,"sid")


def search(input, sender=None, postback=False):
    if postback:
        payload = json.loads(input)
        intent = payload['intent']
        entities = payload['entities']
    else:
        intent, entities = process_query(input)
    if intent is not None:
        if intent in src.__personalized__ and sender is not None:
            r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token' : os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
            })
            entities['sender'] = r.json()
        data = sys.modules['modules.src.' + intent].process(input, entities)
        if data['success']:
            return data['output']
        else:
            if 'error_msg' in data:
                return data['error_msg']
            else:
                return TextTemplate('Something didn\'t work as expected! I\'ll report this to my master.').get_message()
    else:
        return TextTemplate('I\'m sorry; I\'m not sure I understand what you\'re trying to say sir.\nTry typing "help" or "request"').get_message()
