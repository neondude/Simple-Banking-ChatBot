import config
import sqlite3
import re
import createlog

def do_withdraw(username,amount):
    try:
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.execute('Select amount from account where username=?',[username])
        row = cur.fetchone()
        if int(row[0]) < int(amount):
            out_text = "You don't have enought money in your account"
            out_text += "<br> your current account balance is "+ str(row[0])
        else:
            conn.execute('update account set amount = amount - ? where username=?',[amount,username])
            conn.commit()
            createlog.add_log(username,'withdraw',amount)
            out_text = "You have succesfully withdrawn an amount of <strong>"+ str(amount) + "</strong> from your account"
        return out_text
    except Exception as e:
        print
        print
        print e
        print
        print
        return e

def process(user_input, nlu_data):
    try:
        print "module withdraw start"
        print nlu_data
        print type(nlu_data['parameters']['unit-currency'])
        if nlu_data['intent'] == 'withdraw' and nlu_data['parameters']['unit-currency'] != "":
            if type(nlu_data['parameters']['unit-currency']) is dict :
                amount = nlu_data['parameters']['unit-currency']['amount']
            else:
                amount = map(int, re.findall(r'\d+', user_input['user_input_text']))[0]
            out_context = 'None'
            out_text = do_withdraw(user_input['username'],amount)
        elif nlu_data['intent'] == 'withdraw' and nlu_data['parameters']['unit-currency'] == "":
            out_context = "withdraw"
            out_text = "How much money would you like to withdraw from your account?"
        elif nlu_data['intent'] != 'withdraw' and user_input['context'] == 'withdraw':
            amount = map(int, re.findall(r'\d+', user_input['user_input_text']))
            if amount == [] and user_input['user_input_text'].strip().lower() != 'cancel':
                out_context = 'withdraw'
                out_text = "Please specify the amount as an Integer value, or type <em>'cancel'</em> to end the withdraw operation"
            elif user_input['user_input_text'].strip().lower() == 'cancel':
                out_context = 'None'
                out_text = 'withdraw operation has been canceled'
            else:
                out_context = 'None'
                out_text = do_withdraw(user_input['username'],amount[0])
        else:
            out_context = "None"
            out_text = "This is withdraw.py"
        # if nlu_data['intent'] == 'withdraw' and isset_amount(nlu_data):
        #     amount = get_amout(nlu_data)
        #     out_text = do_withdraw(user_input['username'],amount)
        #     out_context = 'None'
        #
        # if nlu_data['intent'] == 'withdraw' and  not isset_amount(nlu_data):
        #     out_context = "withdraw"
        #     out_text = "How much money would you like to withdraw from your account?"
        #
        # elif nlu_data['intent'] != 'withdraw' and user_input['context'] == 'withdraw':
        #     amount = map(int, re.findall(r'\d+', user_input['user_input_text']))[0]
        #     if amount == [] and user_input['user_input_text'].strip().lower() != 'cancel':
        #         out_context = 'withdraw'
        #         out_text = "Please specify the amount as an Integer value, or type <em>'cancel'</em> to end the withdraw operation"
        #     elif user_input['user_input_text'].strip().lower() == 'cancel':
        #         out_context = 'None'
        #         out_text = 'Withdraw operation has been canceled'
        #     else:
        #         out_context = 'None'
        #         out_text = do_withdraw(user_input['username'],amount)
        # else:
        #     out_context = "None"
        #     out_text = "This is withdraw.py"

        output = {
        'bot_response_text': out_text,
        'context': out_context
        }
        return output
    except Exception as e:
        print
        print nlu_data
        print "module withdraw"
        print e
        print
        print
        output = {
        'bot_response_text': str(e),
        'context': 'None'
        }
        return output
