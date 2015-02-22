# -*- coding: utf-8 -*-
import os
from flask import Flask,redirect  
import urllib  
import json
import pymongo
import datetime
from collections import Counter 
from db import getDb

# Replace user and password with API key
user = ""
password = ""

app = Flask(__name__)  

bus = getDb()

@app.route('/')  

def index():  
	return redirect('/stopid/262') 

@app.route('/stopid/<stop>') 

def stopid(stop):
	# Basic doc structure 
	doc= { 
		"stopid" : "id"
	}

	# We store the stopid and the current timestamp
	doc["stopid"] = stop
	doc["timestamp"] = str(datetime.datetime.utcnow())

	print doc 
	# and store the document
	bus.save(doc)

	#realtime bus information
	rturl = "/cgi-bin/rtpi/realtimebusinformation?"
	host = "www.dublinked.ie"
	header = "http://"+user+":"+password+"@"
	rtquery = urllib.urlencode({'stopid': stop, 'operator': 'bac', 'format': 'json'})
	#request url
	request = header + host + rturl + rtquery


	# get file from request
	data = urllib.urlopen(request)	

	# Type: dict  
	wdata = json.load(data)  

	# Print to console/log
	print json.dumps(wdata, indent=2)


	page = '<!doctype html>'
	page +='<head><title>Display all routes for bus stop '+wdata["stopid"]+'</title>'
	page += '<meta http-equiv="refresh" content="60">'
	page += '</head>'
	page += '<body>'

	page +='<h1>Display all routes for bus stop '+wdata["stopid"]+'</h1>'
	page +='<p> Now: '+ wdata["timestamp"]+ '</p>'

	# Our app is lazy, it refuses working during nights...
	if wdata["errorcode"] == "1":
		page +='<p>Sorry, no data for Bus stop '+wdata["stopid"]+' &#95;&#40;&#58;&#1079;&#12301;&ang;&#41;&#95;</p>'

	elif wdata["errorcode"] == "0":

		for i,j in enumerate(wdata["results"], start=1): 
			page += '<h3>#'+ str(i)+'</h3>'
			page += '<p>Route: '+ str(j["route"])+'</p>'
			if j["duetime"] == 'due' or 'Due':
				page += '<p>Due in: '+ str(j["duetime"])+'</p>'
			else: 	 	   
				page += '<p>Due in: '+ str(j["duetime"])+'min </p>'  
			page += '<p>From: '+ str(j["origin"])+'</p>'  
			page += '<p>To: '+str(j["destination"])+'</p>'

	else:
		page +='<p>Hey, are you sure you got internet connected?'+' &#95;&#40;&#58;&#1079;&#12301;&ang;&#41;&#95;</p>'

	# Gather information from database about which stop was requested how many times 
	stopid = sorted([item["stopid"] for item in bus.find()])

	# Get a Counter object for buslist
	c = Counter(stopid)

	# Return a list of the most common elements and their counts from the most common to the least.
	counter = c.most_common()
	page += '<br/><h3>Total requests so far: '+ str(sum(c.values())) +'</h3>'
	for item in counter:
		page += "<p>Stop #"+ item[0] + ":  " + str(item[1]) + "</p>"


	# Finish the page structure and return it 
	page += '<hr>'
	page += '<br/><br/>Data by <a href="http://dublinked.ie">Dublinked</a>'
	page += '</body>'  

	return page  

port = os.getenv('VCAP_APP_PORT', '8911')  

if __name__ == "__main__":  
  app.run(host='0.0.0.0', port=int(port)) 
