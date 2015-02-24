from flask import Flask, render_template, request, redirect
import os
from get import getData, getDb, getAddress, getAllRoutes, getAllStops, getDirections, getStopList

app = Flask(__name__)

# get a collection called "bus"
bus = getDb()

@app.route('/', methods=['GET', 'POST'])
def index():
    totalrequests = bus.count()
    allstops = getAllStops()
    errorcode = 0
    stopid = ""
    
    if request.method == "POST":
        # get stopid that the user has entered
        stopid = request.form['stopid']

        if stopid in allstops:
            errorcode = 0
            return redirect('/stop/' + stopid)

        else:
            errorcode = 1
    
    return render_template('index.html', totalrequests=totalrequests, stopid=stopid, errorcode=errorcode)

@app.route('/stop/<stopid>', methods=['GET', 'POST'])
def stop(stopid):
    bus_results = []
    timestamp = ""
    stopAddress = ""
    bus_doc = {}
    totalrequests = bus.count()
    errorcode = 0
    
    # Type: json
    data = getData(stopid)
    
    # get error code
    errorcode = int(data["errorcode"])
    print errorcode
    
    bus_doc["stopid"] = str(stopid)
    bus_doc["timestamp"] = data["timestamp"]
    bus_doc["clientIP"] = request.remote_addr
    bus_doc["errorcode"] = errorcode
    
    print bus_doc
    
    bus.save(bus_doc)
    
    totalrequests = bus.count()
    
    # get bus results
    if errorcode == 0:
        # get bus stop address
        stopAddress = getAddress(stopid)
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
    
    return render_template('stop.html', results=bus_results, stop=stopid, timestamp=timestamp, errorcode=errorcode, stopAddress=stopAddress, totalrequests=totalrequests)

#new
@app.route('/routelist', methods=['GET', 'POST'])
def routelist():
    totalrequests = bus.count()
    routelist = getAllRoutes()
    errorcode = 0
    route = ""

    if request.method == "POST":
        route = request.form['routelist']

        if route in routelist:
            errorcode = 0
            return redirect('/route/' + route) 
        else:
            errorcode = 1
            
    
    return render_template('routelist.html', totalrequests=totalrequests, route=route, routelist=routelist, errorcode=errorcode)


@app.route('/route/<route>', methods=['GET', 'POST'])
def route(route):
    totalrequests = bus.count()
    directions = getDirections(route)

    if request.method == "POST":
        direction = request.form['direction']
        direction = directions.index(direction)
        print direction

        if direction in [0, 1]:
            return redirect('/route/' + route + '/' + str(direction))

    return render_template('route.html', totalrequests=totalrequests, route=route, directions=directions)

@app.route('/route/<route>/<direction>', methods=['GET', 'POST'])
def direction(route, direction):
    totalrequests = bus.count()
    directions = getDirections(route)
    direction_str = directions[int(direction)]

    stoplist = getStopList(route, direction_str)

    if request.method == "POST":
        stopid = request.form['stopid']

        if route:
            return redirect('/stop/' + stopid) 


    return render_template('direction.html', totalrequests=totalrequests, route=route, direction=direction, direction_str=direction_str, stoplist=stoplist)

@app.route('/map', methods=['GET', 'POST'])
def map():
    totalrequests = bus.count()

    return render_template('map.html', totalrequests=totalrequests)

@app.route('/about')
def about():

    return render_template('about.html')

port = os.getenv('VCAP_APP_PORT', '8901')

if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=int(port))
