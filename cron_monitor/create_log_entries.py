#/usr/bin/python3

#Python script to run cron task daily to create database log entries

from cron_monitor import app
from log_parser import LogParser
from datetime import datetime,timedelta
from flask_mysqldb import MySQL
from flask import Flask, g
import config
end_time = datetime.now()
start_time = end_time - timedelta(days=1)

ctx = app.app_context()
ctx.push()

app.config['MYSQL_USER'] = config.MYSQL_DATABASE_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DATABASE_DB
app.config['MYSQL_HOST'] = config.MYSQL_DATABASE_HOST
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
g.mysql_db = mysql.connection
lp = LogParser(start_time, end_time)
result = lp.parse()