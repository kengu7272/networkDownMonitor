import netifaces
import subprocess
from re import findall
import time

PING_INTERVAL = 5 # This is in seconds
FAILURE = 0.2 # This is in seconds

def getDefaultGateway():
    gateways = netifaces.gateways()
    defaultGateway = gateways['default'][netifaces.AF_INET][0]
    return defaultGateway

def ping(host):
    try:
        output = subprocess.run(f"ping {host} -n 1", capture_output = True, text = True, timeout = FAILURE, shell = True)
        data = output.stdout

        if findall("TTL", data):
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False

timeFailed = 0
lastFailed = None
start = time.time()

defaultGateway = getDefaultGateway()

locationsFile = open('pingLocations.txt', 'r')
locations = locationsFile.readlines()


while(True):
    for server in range(len(locations)):
        while(not ping(defaultGateway)):
            print("LAN is down - no connection to default gateway")
            time.sleep(PING_INTERVAL)
            continue

        time.sleep(PING_INTERVAL)

        
