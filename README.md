# dnsMxRecordTtlChecker
Simple script to scan through all the DNS servers and request for mx records for a specific domain so that you can see the mx record change propagating.

# Dependencies
Python 3
dig

# Installation
Download/clone dnsttl.py and countries into a directory.

# Execution
dnsttl.py <hostname> 

# Output
for each country scanned a csv file with the country code is created.
