# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, render_template
import urllib  
import json
import datetime
from collections import Counter 

from get import getDb, getData

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

    # Type: json
    data = getData(stop)

    # Print to console/log
    print json.dumps(data, indent=2)

    errorcode = int(data["errorcode"])

    bus_entries = []
    if data["errorcode"] == "0":
        for i,j in enumerate(data["results"], start=1):
            bus_entry = {}
            bus_entry["id"] = str(i)
            bus_entry["route"] = str(j["route"])
            bus_entry["duetime"] = str(j["duetime"])
            bus_entry["origin"] = str(j["origin"])
            bus_entry["destination"] = str(j["destination"])
            bus_entries.append(bus_entry)
    
    # for testing purpose
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
    
    # for testing purpose
    print stop_doc["stopid"]
    print stop_doc["timestamp"]
    print bus_entries
    print req_total
    print "database_info:"
    print database_info

    return render_template("stopid.html", 
                            stopid=stop,
                            errorcode = errorcode,
                            timestamp=stop_doc["timestamp"],
                            entries=bus_entries,
                            req_total=req_total,
                            requests=database_info)

port = os.getenv('VCAP_APP_PORT', '8901')

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=int(port))
