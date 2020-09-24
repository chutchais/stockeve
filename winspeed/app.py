from flask import Flask,request ,make_response,g#, url_for
import time
import json
import datetime

from flask import request
from flask import Response

# import requests
# import json
# from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test():
	jdata ={"key":"sdasdas"}
	return json.dumps(jdata, indent=4,sort_keys=True) ,200

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
