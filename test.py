from get import getAllRoutes, getAllStops, getDirections, getStopList, getLocation, getAllLocations

routelist = getAllRoutes()

print routelist
print len(routelist)

for i in routelist[0:10]:
	print routelist.index(i)
	print getDirections(i)

#route = "1"
#direction = "From Santry via O'Connell Street to Sandymount"

#stoplist = getStopList(route, direction)

#print stoplist

#allstops = getAllStops()

#print allstops

stopid = 262

print getLocation(stopid)

fakeid = 1

print getLocation(fakeid)

print getAllLocations()

