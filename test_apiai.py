import json
import requests

API_AI_CLIENT_KEY = 'adc3604824c5464eb12ffd50de74cf32 '


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
