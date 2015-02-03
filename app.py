# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, render_template
import urllib  
import json
import datetime
from collections import Counter 
from db import getDb

# Replace user and password with API key
user = "linqi"
password = "1710qi2014"

app = Flask(__name__)  

bus = getDb()

@app.route('/')  


def index():  
    return redirect('/stopid/262')


@app.route('/stopid/<stop>') 


def stopid(stop):
    # doc for bus stop
    stop_doc= {
        "stopid" : "id"
    }

    # We store the stopid and the current timestamp
    stop_doc["stopid"] = str(stop)
    stop_doc["timestamp"] = str(datetime.datetime.utcnow())


    print stop_doc
    # and store the document
    bus.save(stop_doc)

    # realtime bus information
    rturl = "/cgi-bin/rtpi/realtimebusinformation?"
    host = "www.dublinked.ie"
    header = "http://"+user+":"+password+"@"
    rtquery = urllib.urlencode({'stopid': stop, 'operator': 'bac', 'format': 'json'})

    # request url
    request = header + host + rturl + rtquery

    # get file from request
    data = urllib.urlopen(request)

    # Type: dict
    wdata = json.load(data)

    # Print to console/log
    print json.dumps(wdata, indent=2)

    # doc structure for bus information

    #page = '<!doctype html><html>'
    #page += '<head><title>Display all routes for bus stop '+wdata["stopid"]+'</title>'
    #page += '<meta http-equiv="refresh" content="60">'
    #page += '</head>'
    #page += '<body>'

   # page +='<h1>Display all routes for bus stop '+wdata["stopid"]+'</h1>'
   # page +='<p> Now: '+ wdata["timestamp"]+ '</p>'

    errorcode = int(wdata["errorcode"])


    # Our app is lazy, it refuses working during nights...
    #if wdata["errorcode"] == "1":
    #    page += '<p>Sorry, no data for Bus stop ' + wdata["stopid"] + ' &#95;&#40;&#58;&#1079;&#12301;&ang;&#41;&#95;</p>'

    #elif wdata["errorcode"] == "0":
    bus_entries = []
    if wdata["errorcode"] == "0":
        for i,j in enumerate(wdata["results"], start=1):
            bus_entry = {}
            bus_entry["id"] = str(i)
            bus_entry["route"] = str(j["route"])
            bus_entry["duetime"] = str(j["duetime"])
            bus_entry["origin"] = str(j["origin"])
            bus_entry["destination"] = str(j["destination"])
            bus_entries.append(bus_entry)
            #page += '<div><h3>#'+ str(i)+'</h3>'
            #page += '<p>Route: '+ str(j["route"])+'</p>'
            #if j["duetime"] == 'due' or 'Due':
            #    page += '<p>Due in: '+ str(j["duetime"])+'</p>'
            #else:
            #    page += '<p>Due in: '+ str(j["duetime"])+'min </p>'
            #page += '<p>From: '+ str(j["origin"])+'</p>'
            #page += '<p>To: '+str(j["destination"])+'</p></div>'
    print "HERE"
    # Gather information from database about which stop was requested how many times
    stopid_list = sorted([item["stopid"] for item in bus.find()])

    # Get a Counter object for buslist
    c = Counter(stopid_list)

    # Return a list of the most common elements and their counts from the most common to the least.
    counter = c.most_common()
    print counter

    req_total = sum(c.values())
    #page += '<br><br><div><h3>Total requests so far: '+ str(sum(c.values())) +'</h3>'

    database_info = []
    for item in counter:
        bus_info = {}
        bus_info["stop"] = item[0]
        bus_info["sum"] = item[1]
        database_info.append(bus_info)
        #page += "<p>Stop #"+ item[0] + ":  " + str(item[1]) + "</p>"
    #page += '</div>'

    # Finish the page structure and return it
    #page += '<hr>'
    #page += 'Data by <a href="http://dublinked.ie">Dublinked</a>'
    #page += '</body></html>'

    print stop_doc["stopid"]
    print stop_doc["timestamp"]
    print bus_entries
    print req_total
    print "database_info:"
    print database_info

    return render_template("index.html", 
                            stopid=stop,
                            errorcode = errorcode,
                            timestamp=stop_doc["timestamp"],
                            entries=bus_entries,
                            req_total=req_total,
                            requests=database_info)

port = os.getenv('VCAP_APP_PORT', '8901')

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=int(port))
