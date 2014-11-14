# -*- coding: utf-8 -*-

import re
import os  
import pymongo

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
		db = db.name(mongodb_uri)
		bus = client[db].dublinbus
		return bus

	# or we are local  
	else:  
		mongodb_uri = 'mongodb://localhost:27017/'
		client = pymongo.MongoClient(mongodb_uri)
		# Create the 'dublinbus' collection
		bus = client.bus.dublinbus01
		return bus