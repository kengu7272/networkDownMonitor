import netifaces
import time
from ping3 import ping as p

PING_INTERVAL = 5 # This is in seconds
FAILURE = 0.2 # This is in seconds

def getDefaultGateway():
    gateways = netifaces.gateways()
    defaultGateway = gateways['default'][netifaces.AF_INET][0]
    return defaultGateway

def ping(host):
    result = p(host, timeout = FAILURE)

    if result is not None:
        return result
    
    return False

timeFailed = 0
lastFailed = None
start = time.time()

defaultGateway = getDefaultGateway()

locationsFile = open('pingLocations.txt', 'r')
locations = locationsFile.readlines()

try:
    while(True):
        for server in range(len(locations)):
            ms = ping(locations[server])

            if(not ms):
                up = False

                for i in range(len(locations)):
                    if(ping(locations[i])):
                        up = True

                if(not up):
                    print("Network down")
                    failStart = time.time()
                    elapsed = None

                    # if connection to default gateway is not found (LAN failure)
                    if(not p(defaultGateway)):
                        print("LAN is down - no connection to default gateway")
                        while(not ping(defaultGateway)):
                            pass
                        elapsed = time.time() - failStart
                    else:
                        while(not ms):
                            for i in range(len(locations)):
                                ms = ping(locations[i])
                        elapsed = time.time() - failStart

                    print(f"Network back up, down for {elapsed} seconds")

            print(f"Ping to {locations[server]} took {round(ms * 1000, 0)}ms")
            time.sleep(PING_INTERVAL)
except KeyboardInterrupt:
    print("User stopped program")

        
