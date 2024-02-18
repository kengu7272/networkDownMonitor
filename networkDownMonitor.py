import netifaces
import time
from ping3 import ping as p
import os
from datetime import datetime
from tzlocal import get_localzone

PING_INTERVAL = 5 # This is in seconds
FAILURE = 0.2 # This is in seconds

def getDefaultGateway():
    gateways = netifaces.gateways()
    defaultGateway = gateways['default'][netifaces.AF_INET][0]
    return defaultGateway

def ping(host):
    try: 
        result = p(host, timeout = FAILURE)

        if result is not None:
            return result
        
        return False
    except:
        return False
    

def writeOutput(text):
    with open('failures.txt', 'a') as output:
        output.write(text)

def timestampToDatetime(timestamp):
    dto = datetime.fromtimestamp(timestamp, get_localzone())
    return dto.strftime('%Y-%m-%d %H:%M:%S %Z')

start = time.time()
writeOutput(f"Network test started at {timestampToDatetime(start)}\n\n")
defaultGateway = getDefaultGateway()

with open('pingLocations.txt', 'r') as locationsFile:
    locations = [line.strip() for line in locationsFile.readlines()]

try:
    while(True):
        for server in range(len(locations)):
            ms = ping(locations[server].strip())

            if(not ms):
                up = False

                for i in range(len(locations)):
                    if(ping(locations[i].strip())):
                        up = True

                if(not up):
                    print("Network down")
                    failStart = time.time()
                    elapsed = None

                    # if connection to default gateway is not found (LAN failure)
                    if(not ping(defaultGateway)):
                        writeOutput(f"LAN failure at {timestampToDatetime(failStart)}\n")                       
                        print("LAN is down - no connection to default gateway ")

                        while(not ping(defaultGateway)):
                            pass

                        elapsed = time.time() - failStart
                        writeOutput(f"Down for about {int(elapsed)} seconds\n\n")
                    else:
                        writeOutput(f"WAN failure at {timestampToDatetime(failStart)}\n")
                        print("WAN failure, can't connect to any servers")

                        while(not ms):
                            for i in range(len(locations)):
                                ms = ping(locations[i].strip())

                        elapsed = time.time() - failStart
                        writeOutput(f"Down for about {int(elapsed)} seconds\n\n")


            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Network is up")
            time.sleep(PING_INTERVAL)
except KeyboardInterrupt:
    print(f"User stopped program - Program ran for {int(time.time() - start)} seconds")
    writeOutput(f"Network test ended at {timestampToDatetime(time.time())}\n\n")

        
