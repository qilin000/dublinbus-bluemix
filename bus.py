import time
import sched
from threading import Timer
from pymongo import MongoClient
import pymongo
import datetime
from collections import Counter 

# Replace user and password with API key
user = "linqi"
password = "1710qi2014"

app = Flask(__name__)  

# Get service information if on Bluemix  
if 'VCAP_SERVICES' in os.environ:  
	mongoInfo = json.loads(os.environ['VCAP_SERVICES'])['mongolab'][0]  
	mongodb_uri = mongoInfo['credentials']['uri']
	client = pymongo.MongoClient(mongodb_uri)
	# Create the 'dublinbus' collection in 'IbmCloud_queosken_kiqc0i9g' database in Mongolab
	# WARNING: need to change db name everytime push to new app
	bus = client.IbmCloud_queosken_d9ure9tq.dublinbus
	
# or we are local  
else:  
	mongodb_uri = 'mongodb://localhost:27017/'
	client = pymongo.MongoClient(mongodb_uri)
	# Create the 'dublinbus' collection
	bus = client.bus.dublinbus01


s = sched.scheduler(time.time, time.sleep)

def print_something(sc):
	#time.sleep(-time.time() % 60)
	# Output some testing data to console/log
	stopid = sorted([item["stopid"] for item in bus.find()])
	counter = Counter(stopid).most_common()
	print ">>>>>>Output some testing data to console/log<<<<<<"
	print "Total requests: " + str(bus.count())
	for item in counter:
		print "Route "+ item[0] + ": " + str(item[1])
	print ">>>>>>End of testing data<<<<<<"
	sc.enter(2, 1, print_something, (s,))

s.enter(2, 1, print_something, (s,))
s.run()

def print_with_time():
	Timer(5, print_something, ()).start()
	#time.sleep(-time.time() % 60)
	time.sleep(1)

