import sqlite3

try:
    conn = sqlite3.connect('Banker.db')
    conn.execute("CREATE TABLE IF NOT EXISTS `userdb` (	`username`	TEXT,	`password`	TEXT NOT NULL,	PRIMARY KEY(`username`));")
    conn.execute("CREATE TABLE `account` (	`username`	TEXT NOT NULL,	`amount`	REAL,	PRIMARY KEY(`username`));")

except Exception as e:
    print e
