from flask import Flask, render_template, request
import os
import json

from get import getData, getDb
from webcrawler import crawl

app = Flask(__name__)

# get a collection called "bus"
bus = getDb()


@app.route('/', methods=['GET', 'POST'])
def index():
    inputs = []
    bus_results = []
    stop = ""
    address = ""
    timestamp = ""
    errorcode = 2
    stopAddress = ""
    bus_doc = {}
    totalrequests = bus.count()
    
    
    if request.method == "POST":
        # get url that the user has entered
        stop = request.form['stopid']
        inputs.append(stop)

    if inputs:
        #get stop
        stop = inputs.pop()
        
        # Type: json
        data = getData(stop)
        
        # get error code
        errorcode = int(data["errorcode"])
        print errorcode
        
        bus_doc["stopid"] = str(stop)
        bus_doc["timestamp"] = data["timestamp"]
        bus_doc["clientIP"] = request.remote_addr
        bus_doc["errorcode"] = errorcode
        
        print bus_doc
        
        bus.save(bus_doc)
        
        totalrequests = bus.count()
        

        
        # get bus results
        if errorcode == 0:
            # get bus stop address
            stopAddress = crawl(stop)
            # get timestamp
            timestamp = data["timestamp"]
            for i,j in enumerate(data["results"], start=1):
                bus_result = {}
                bus_result["id"] = str(i)
                bus_result["route"] = str(j["route"])
                bus_result["duetime"] = str(j["duetime"])
                bus_result["origin"] = str(j["origin"])
                bus_result["destination"] = str(j["destination"])
                bus_results.append(bus_result)
        
        #print "====================BUS INFORMATION==================="
        # Print to console/log
        #print json.dumps(data, indent=2)
    
    return render_template('index.html', results=bus_results, stop=stop, timestamp=timestamp, errorcode=errorcode, stopAddress=stopAddress, totalrequests=totalrequests)

@app.route('/about')
def about():
    return render_template('about.html')

port = os.getenv('VCAP_APP_PORT', '8901')

if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=int(port))
