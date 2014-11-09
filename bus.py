import os  
from flask import Flask,redirect  
import urllib  
import json 

#Replace user and password with API key
user = "username"
password = "password"

BASE_URL = """http://"""+user+":"+password+"""@
	www.dublinked.ie
	/cgi-bin/rtpi/realtimebusinformation?stopid="""

app = Flask(__name__)  

@app.route('/')  

def index():  
	return redirect('/stopid/262') 

@app.route('/stopid/<stop>') 

def stopid(stop):
	
	#Replace user and password with API key
	user = "linqi"
	password = "1710qi2014"

	#default request
	request = """http://"""+user+":"+password+"""@
	www.dublinked.ie
	/cgi-bin/rtpi/
	realtimebusinformation?stopid=1&operator=bac
	"""

	#realtime bus information
	rturl = "/cgi-bin/rtpi/realtimebusinformation?"
	host = "www.dublinked.ie"
	header = "http://"+user+":"+password+"@"
	rtquery = urllib.urlencode({'stopid': stop, 'operator': 'bac', 'format': 'json'})
	#request url
	request = header + host + rturl + rtquery


	# get file from request
	data = urllib.urlopen(request)	  
	wdata = json.load(data)  
	print json.dumps(wdata, indent=2)  
	page='<title>Display all routes for bus stop'+wdata["stopid"]+'</title>'  
	page +='<h1>Display all routes for bus stop '+wdata["stopid"]+' (timestamp: '+wdata["timestamp"]+')</h1>'

	for i,j in enumerate(wdata["results"], start=1): 
			page += '<h3>#'+ str(i)+'</h3>'
			page += '<p>Route: '+ str(j["route"])+'</p>'   
			page += '<p>Due in: '+ str(j["duetime"])+'min </p>'  
			page += '<p>From: '+ str(j["origin"])+'</p>'  
			page += '<p>To: '+str(j["destination"])+'</p>' 

	return page  

port = os.getenv('VCAP_APP_PORT', '5000')  

if __name__ == "__main__":  
  app.run(host='0.0.0.0', port=int(port)) 
