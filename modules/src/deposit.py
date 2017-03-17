# def process(user_input, nlu_data):
#     out_text = 'this is deposit.py'
#     output = {
#         'bot_response_text': out_text,
#         'context': 'None'
#     }
#     return output

import config
import sqlite3
import re
import createlog

def do_deposit(username,amount):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute('update account set amount = amount + ? where username=?',[amount,username])
        conn.commit()
        createlog.add_log(username,'deposit',amount)
        out_text = "You have succesfully deposited an amount of <strong>"+ str(amount) + "</strong> into your account"
        return out_text
    except Exception as e:
        print
        print e
        print
        return e


def process(user_input, nlu_data):
    try:
        if nlu_data['intent'] == 'deposit' and nlu_data['parameters']['unit-currency'] != "":
            if type(nlu_data['parameters']['unit-currency']) is dict :
                amount = nlu_data['parameters']['unit-currency']['amount']
            else:
                amount = map(int, re.findall(r'\d+', user_input['user_input_text']))[0]
            out_context = 'None'
            out_text = do_deposit(user_input['username'],amount)
        elif nlu_data['intent'] == 'deposit' and nlu_data['parameters']['unit-currency'] == "":
            out_context = "deposit"
            out_text = "How much money would you like to deposit into your account?"
        elif nlu_data['intent'] != 'deposit' and user_input['context'] == 'deposit':
            amount = map(int, re.findall(r'\d+', user_input['user_input_text']))
            if amount == [] and user_input['user_input_text'].strip().lower() != 'cancel':
                out_context = 'deposit'
                out_text = "Please specify the amount as an Integer value, or type <em>'cancel'</em> to end the deposit operation"
            elif user_input['user_input_text'].strip().lower() == 'cancel':
                out_context = 'None'
                out_text = 'deposit operation has been canceled'
            else:
                out_context = 'None'
                out_text = do_deposit(user_input['username'],amount[0])
        else:
            out_context = "None"
            out_text = "This is deposit.py"

        output = {
        'bot_response_text': out_text,
        'context': out_context
        }
        return output
    except Exception as e:
        print
        print "module deposit"
        print e
        print
        output = {
        'bot_response_text': str(e),
        'context': 'None'
        }
        return output
