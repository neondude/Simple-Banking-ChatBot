from datetime import datetime
import time
import config
import sqlite3
# print datetime.strptime('2017-03-14', '%Y-%m-%d')
# print time.mktime(d.timetuple())
def get_summary(username,count=10):
    try:
        summary_list = []
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.execute('select amount,action,id from logs where username=? order by timestamp desc limit ?',[username,count])
        for row in cur.fetchall():
            summary_list.append({
            'amount' : row[0],
            'action' : row[1],
            'id' : row[2]
            })
        return summary_list
    except Exception as e:
        print
        print e
        print
        return e

def get_list_html(summary_list):
    list_html = ""
    for item in summary_list:
        list_html += '<tr>'
        list_html += '<td>' + str(item['id']) + '</td>'
        list_html += '<td>' + str(item['action']) + '</td>'
        list_html += '<td>' + str(item['amount']) + '</td>'
        list_html += '</tr>'
    return list_html



def process(user_input, nlu_data):
    count = 10
    if nlu_data['parameters']['number'] !='':
        count = int(nlu_data['parameters']['number'])
        out_text ="The Last "+ str(count)  +" transactions on your account"
    else:
        out_text ="The Last few transactions on your account"

    summary_list = get_summary(user_input['username'],count)
    out_text += '''<table class="table table-condensed">
    <thead>
      <tr>
        <th>TXN ID</th>
        <th>Action</th>
        <th>Amount</th>
      </tr>
    </thead>
    <tbody>'''

    out_text += get_list_html(summary_list)

    out_text +='''
    </tbody>
  </table>'''

    output = {
        'bot_response_text': out_text,
        'context': 'None'
    }
    return output
