import urllib  
import json
import re
import os  
import pymongo

# Replace user and password with API key
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

def db_name(uri):
	#uri = "mongodb://IbmCloud_queosken_d9ure9tq_8me846fu:PTRo6ZoIZb7L6tR1NuSMfGld4iN3fskC@ds049570.mongolab.com:49570/IbmCloud_queosken_d9ure9tq"

	result = re.split(r'/', uri)
	return result[-1]

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