from flask import Flask,request ,make_response,g#, url_for
import time
import json
import datetime

from flask import request
from flask import Response

import os
import sys
from typing import List, Tuple

import pyodbc

CONNECTION_STRING: str = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

app = Flask(__name__)

def connect_db() -> pyodbc.Connection:
    ''' Connect to database. '''
    print('Establishing mssql database connection.')
    connection_str = CONNECTION_STRING.format(
        server='192.168.101.1',
        database='dbwins_EMG',
        username='sa',
        password='SYSsql##'
    )

    return pyodbc.connect(connection_str, timeout=100)

def fetch_data(sql,cur: pyodbc.Cursor) -> List:
    ''' Fetch all data from the table. '''
    print('List of data.')
    cur.execute(sql)

    return cur.fetchall()

@app.route('/', methods=['GET'])
def index():
	jdata ={"key":"sdasdas"}
	return json.dumps(jdata, indent=4,sort_keys=True) ,200


@app.route('/api/check_db_connection', methods=['GET'])
def check_db_connection():
	try:
		conn = connect_db()
		jdata ={
			"status":"Connection is sucessful"}
		conn.close()
	except Exception as e :
		jdata ={
			"status":f"Unable to connect database : {e}"
			}
	return json.dumps(jdata, indent=4,sort_keys=True) ,200

@app.route('/api/invoice/<invoice>', methods=['GET'])
def fetch_invoice(invoice):
	try:
		conn = connect_db()
		cur = conn.cursor()
		sql = f"select soinvid from [dbwins_EMG].[dbo].[SOInvDT] where soinvid={invoice}"
		rows = fetch_data(sql,cur)
		jdata ={
			"sql" : sql,
			"rows" : 1,
			"status":"Fetch is sucessful"}
		cur.close()
		conn.close()
	except Exception as e :
		jdata ={
			"sql" : sql,
			"status":f"Unable to connect database : {e}"
			}
	return json.dumps(jdata, indent=4,sort_keys=True) ,200

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)