from flask import Flask, render_template, request
import os
import json

from get import getData

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    inputs = []
    bus_results = []
    stop = ""
    address = ""
    timestamp = ""
    errorcode = 2
    numberofresults = 0
    
    if request.method == "POST":
        # get url that the user has entered
        stop = request.form['stopid']
        inputs.append(stop)

    if inputs:
        #get stop
        stop = inputs.pop()
        
        # Type: dict
        data = getData(stop)
        
        # get error code
        errorcode = int(data["errorcode"])
        print errorcode
        
        # get bus address
        numberofresults = str(data["numberofresults"])
        
        # get bus results
        if errorcode == 0:
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
    
    return render_template('index.html', results=bus_results, stop=stop, timestamp=timestamp, errorcode=errorcode, numberofresults=numberofresults)

@app.route('/about')
def about():
    return render_template('about.html')

port = os.getenv('VCAP_APP_PORT', '8901')

if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=int(port))
