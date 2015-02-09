import urllib  
import json 

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
