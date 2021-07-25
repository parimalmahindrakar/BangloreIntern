import urllib.request
def internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
# test
print( "connected" if internet_connection() else "No Internet!" )