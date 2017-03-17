import config
import sqlite3
import time

def add_log(username,action,amount):
    try:
        timestamp = int(time.time())
        conn = sqlite3.connect(config.DATABASE)
        conn.execute('insert into logs (username,amount,action,timestamp) values (?,?,?,?)',[username,amount,action,timestamp])
        conn.commit()
    except Exception as e:
        print
        print 'add_log'
        print e
        print

def chatlog(username,message,sender):
    try:
        timestamp = int(time.time())
        conn = sqlite3.connect(config.DATABASE)
        conn.execute('insert into chatlog (username,message,sender) values (?,?,?)',[username,message,sender])
        conn.commit()
    except Exception as e:
        print
        print 'chatlog'
        print e
        print
