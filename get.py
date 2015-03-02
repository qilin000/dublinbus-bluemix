import urllib  
import json
import re
import os  
import pymongo

# Remove user and password with API key
user = ""
password = ""

def getData(stopid):
    # realtime bus information
    rturl = "/cgi-bin/rtpi/realtimebusinformation?"
    host = "www.dublinked.ie"
    header = "http://"+user+":"+password+"@"
    rtquery = urllib.urlencode({'stopid': stopid, 'operator': 'bac', 'format': 'json'})

    # request url
    request = header + host + rturl + rtquery

    # get file from request
    data = urllib.urlopen(request)

    # Type: dict
    wdata = json.load(data)
    
    return wdata


# Retrieve address given a specific bus stop
def getAddress(stopid):

    # get data
    stopaddress_json = open("./static/json/stopaddress.json")
    stopaddress = json.load(stopaddress_json, object_hook=_decode_dict)
    stopaddress_json.close()

    for i in stopaddress:
        if int(stopid) == int(i["stopid"]):
            result = i["address"]
            break 
        else:
            result = "N/A"

    return result 

    # return String
    
# Decode hood
def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


# return a list of all stops available
def getAllStops():
    result = []
    # get data
    stopaddress_json = open("./static/json/stopaddress.json")
    stopaddress = json.load(stopaddress_json, object_hook=_decode_dict)
    stopaddress_json.close()

    for i in stopaddress:
        result.append(str(i["stopid"]))

    # a list of Strings
    return result 


# Get database name
def db_name(uri):
    # uri = "mongodb://IbmCloud_mmqbqveq_l91282ub_gcs904fk:A5np9uykPs_v00n5tdrKwUXviKQ27uAK@ds055200.mongolab.com:55200/IbmCloud_mmqbqveq_l91282ub"

    result = re.split(r'/', uri)
    return result[-1]


# Get a collection
def getDb():
    # Get service information if on Bluemix  
    if 'VCAP_SERVICES' in os.environ:  
        mongoInfo = json.loads(os.environ['VCAP_SERVICES'])['mongolab'][0]  
        mongodb_uri = mongoInfo['credentials']['uri']
        client = pymongo.MongoClient(mongodb_uri)
        # Create the 'dublinbus' collection in 'IbmCloud_queosken_kiqc0i9g' database in Mongolab
        db = db_name(mongodb_uri)
        # Dublinbus collection
        bus = client[db].dublinbus
        return bus

    # or we are local  
    else:  
        mongodb_uri = 'mongodb://localhost:27017/'
        client = pymongo.MongoClient(mongodb_uri)
        # Create the 'dublinbus' collection
        bus = client.bus.dublinbus01
        return bus