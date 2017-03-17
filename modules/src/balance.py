import config
import sqlite3

def get_balance(username):
    try:
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.execute('select amount from account where username=?',[username])
        row = cur.fetchone()
        return row[0]
    except Exception as e:
        print
        print
        print e
        print
        print



def process(user_input, nlu_data):
    account_balance = get_balance(user_input['username'])
    out_text = "The current balance in your account is "+ str(account_balance)
    output = {
        'bot_response_text': out_text,
        'context': 'None'
    }
    return output
