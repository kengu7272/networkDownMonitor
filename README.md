# Simple Network Uptime Monitor
## Use
- Run script using python or if on Windows run "run.bat"
- PING_INTERVAL = How often a ping is sent out to verify network connectivity (default 5 seconds)
- FAILURE = Determines how long a ping must take before it is considered a failure (default 0.2 seconds / 200ms)
- pingLocations.txt - Line separated file for servers to ping to verify WAN connectivity - default has popular DNS servers and such
