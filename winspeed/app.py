from flask import Flask,request ,make_response,g#, url_for
import time
import json
import datetime

from flask import request,jsonify
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
	# return json.dumps(jdata, indent=4,sort_keys=True) ,200
	response=jsonify(jdata)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# Start Sale API
@app.route('/api/sale/date/<day>', methods=['GET'])
def fetch_sale_by_date(day):
	try:
		conn = connect_db()
		cur = conn.cursor()
		sql = f"select SOInvID,DocuNo,TotaBaseAmnt,VATAmnt,NetAmnt from [dbwins_EMG].[dbo].[SOInvHD] where DocuDate='{day}'"
		rows = fetch_data(sql,cur)
		invoices =[]
		for row in rows:
			row_json = {
				'SOInvID': row.SOInvID,
				'DocuNo':row.DocuNo,
				'TotaBaseAmnt': str(row.TotaBaseAmnt),
				'VATAmnt': str(row.VATAmnt),
				'NetAmnt': str(row.NetAmnt)
			}
			invoices.append(row_json)
		jdata ={
			"sql" : sql,
			"rows" : len(rows),
			"status":f"Fetch sale by date on {day} is sucessful",
			"invoices": invoices}
		cur.close()
		conn.close()
	except Exception as e :
		jdata ={
			"sql" : sql,
			"status":f"Unable to fetch data : {e}"
			}
	response=jsonify(jdata)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
	# return json.dumps(jdata, indent=4,sort_keys=True) ,200

@app.route('/api/saleorder/<soid>', methods=['GET'])
def fetch_saleorder(soid):
	try:
		conn = connect_db()
		cur = conn.cursor()
		sql = f"select s.ListNo,s.SOInvID,s.GoodID,s.GoodName,s.GoodQty2,s.GoodAmnt,e.GoodCode,s.InveID,i.InveCode,i.InveName from [dbwins_EMG].[dbo].[SOInvDT] s inner join [dbwins_EMG].[dbo].[EMGood] e on s.GoodID = e.GoodID inner join [dbwins_EMG].[dbo].[EMInve] i on s.InveID = i.InveID  where s.soinvid={soid}"
		# sql = "select s.ListNo,s.SOInvID,s.GoodID,s.GoodName,"\
		# 		"s.GoodQty2,s.GoodAmnt,e.GoodCode ,"\
		# 		"s.InveID,i.InveCode,i.InveName " \
		# 		"from [dbwins_EMG].[dbo].[SOInvDT] s " \ 
		# 			"inner join [dbwins_EMG].[dbo].[EMGood] e " \
		# 			"on s.GoodID = e.GoodID " \
		# 			"inner join [dbwins_EMG].[dbo].[EMInve] i " \
		# 			"on s.InveID = i.InveID " \
		# 		"where s.soinvid=" + str(soid)

		rows = fetch_data(sql,cur)
		items =[]
		for row in rows:
			row_json = {
				'SOInvID': row.SOInvID,
				'GoodCode':row.GoodCode,
				'GoodID':row.GoodID,
				'GoodName':row.GoodName,
				'GoodQty2':str(row.GoodQty2),
				'GoodAmnt': str(row.GoodAmnt),
				'ListNo' : row.ListNo,
				'InveID' : str(row.InveID),
				'InveCode': str(row.InveCode),
				'InveName': row.InveName
			}
			items.append(row_json)
		jdata ={
			"sql" : sql,
			"rows" : len(rows),
			"status":f"Fetch sale order {soid} is sucessful",
			"items": items}
		cur.close()
		conn.close()
	except Exception as e :
		jdata ={
			"sql" : sql,
			"status":f"Unable to connect database : {e}"
			}
	# response=jsonify(jdata)
	# response.headers.add('Access-Control-Allow-Origin', '*')
	# return response
	return json.dumps(jdata, indent=4,ensure_ascii=False).encode('utf8') ,200

@app.route('/api/invoice/<invoice>', methods=['GET'])
def fetch_invoice(invoice):
	try:
		conn = connect_db()
		cur = conn.cursor()
		# sql = f"select s.SOInvID,s.GoodID,s.GoodName,s.GoodQty2,s.GoodAmnt,e.GoodCode from [dbwins_EMG].[dbo].[SOInvDT] s inner join [dbwins_EMG].[dbo].[EMGood] e on s.GoodID = e.GoodID where s.soinvid={invoice}"
		sql = f"SELECT h.DocuNo,d.SOInvID,e.goodid,e.GoodCode,d.GoodName,d.GoodQty2,d.GoodAmnt FROM [dbwins_EMG].[dbo].[SOInvHD] h inner join [dbwins_EMG].[dbo].[SOInvDT] d on h.SOInvID = d.SOInvID inner join [dbwins_EMG].[dbo].[EMGood] e on d.GoodID = e.GoodID where h.DocuNo='{invoice}'" 

		rows = fetch_data(sql,cur)
		items =[]
		for row in rows:
			row_json = {
				'DocuNo':row.DocuNo,
				'SOInvID': row.SOInvID,
				'GoodCode':row.GoodCode,
				'GoodID':row.GoodID,
				'GoodName':row.GoodName,
				'GoodQty2':str(row.GoodQty2),
				'GoodAmnt': str(row.GoodAmnt)
			}
			items.append(row_json)
		jdata ={
			"sql" : sql,
			"rows" : len(rows),
			"status":f"Fetch invoice {invoice}is sucessful",
			"items": items}
		cur.close()
		conn.close()
	except Exception as e :
		jdata ={
			"sql" : sql,
			"status":f"Unable to connect database : {e}"
			}
	# response=jsonify(jdata)
	# response.headers.add('Access-Control-Allow-Origin', '*')
	# return response
	return json.dumps(jdata, indent=4,ensure_ascii=False).encode('utf8') ,200
# End Sale API

# Start PO (Receive) API
@app.route('/api/receive/date/<day>', methods=['GET'])
def fetch_receive_by_date(day):
	try:
		conn = connect_db()
		cur = conn.cursor()
		sql = f"select POInvID,DocuNo,InvNo,ShipNo,PONo,TotaBaseAmnt,VATAmnt,NetAmnt,VendorName from [dbwins_EMG].[dbo].[POInvHD] where DocuDate='{day}'"
		rows = fetch_data(sql,cur)
		pos =[]
		for row in rows:
			row_json = {
				'POInvID': row.POInvID,
				'DocuNo':row.DocuNo,
				'InvNo':row.InvNo,
				'ShipNo':row.ShipNo,
				'PONo':row.PONo,
				'VendorName':row.VendorName,
				'TotaBaseAmnt': str(row.TotaBaseAmnt),
				'VATAmnt': str(row.VATAmnt),
				'NetAmnt': str(row.NetAmnt)
			}
			pos.append(row_json)
		jdata ={
			"sql" : sql,
			"rows" : len(rows),
			"status":f"Fetch receive by date on {day} is sucessful",
			"pos": pos}
		cur.close()
		conn.close()
	except Exception as e :
		jdata ={
			"sql" : sql,
			"status":f"Unable to fetch data : {e}"
			}
	response=jsonify(jdata)
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers["Content-Type"] = "text/json; charset=utf-8"
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
