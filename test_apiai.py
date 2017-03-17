import json
import requests

API_AI_CLIENT_KEY = 'adc3604824c5464eb12ffd50de74cf32 '


# def process_query(user_input,sessionid):
#     try:
#         #r = requests.post('https://api.api.ai/v1/query?v=20170310&'+ 'query=' + user_input+'&lang=en&sessionId='+sessionid + '&e=READ_AMOUNT' ,
#         r = requests.post('https://api.api.ai/v1/query?v=20170310&',
#                          headers={
#                              'Authorization': 'Bearer %s' % API_AI_CLIENT_KEY,
#                              'Content-Type': "application/json; charset=utf-8"
#                              },
#                           data = {
#                                'lang' : 'en',
#                                'sessionId' : sessionid,
#                                "event":{
#                                    "name":"READ_AMOUNT",
#                                    "data":{
#                                        'unit-currency': user_input
#                                        }
#                                    }
#                               }
#                          )
#         data = r.json()
#         return data
#     except  Exception as e:
#         return e

def process_query(user_input,sessionid):
    try:
        #r = requests.post('https://api.api.ai/v1/query?v=20170310&'+ 'query=' + user_input+'&lang=en&sessionId='+sessionid + '&e=READ_AMOUNT' ,
        r = requests.post('https://api.api.ai/v1/query?v=20170310&',
                         headers={
                             'Authorization': 'Bearer %s' % API_AI_CLIENT_KEY,
                             'Content-Type': "application/json; charset=utf-8"
                             },
                          data = json.dumps({'event':{ 'name': 'READ_AMOUNT', 'data': {'money': '2 million'}}, 'timezone':'America/New_York', 'lang':'en', 'sessionId':'1321321'})
                         )
        data = r.json()
        return data
    except  Exception as e:
        return e


if __name__ == '__main__':
    print process_query("2 million" ,"sid")
