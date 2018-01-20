# Small script to scan through all the DNS Servers in the world and query for TTL of a given domain.
# Usage dnsttl.py hostname

import sys
import requests
import multiprocessing
import subprocess

def main():

    hostname = ""
    filename = sys.argv[0].split("/")
    filename.reverse()
    filename = filename[0]

    if len(sys.argv) == 2:
        hostname = sys.argv[1]

    else:
        print("Usage: py {0} hostname [-v]".format(filename))
        exit()


    #Load the list of countries into an array
    countries = []
    with open("countries", "r") as countries_file:
        for line in countries_file:
            words = line.split()
            countries.append(words[0].lower())


    #For each country, get a list of DNS servers.
    #can Consider multiprocessing by country as well if computer is powerful enough.
    for c in countries:
        # https://public-dns.info/nameserver/<COUNTRY CODE>.txt
        d = requests.get("https://public-dns.info/nameserver/{0}.txt".format(c)).text.split()

        # For each DNS server, dig to get the records for the host name.
        with open(c+".csv", "w") as outfile:
            outfile.write("Server, Domain, TTL, IN, Type, Priority, Result\n")
            # Multiprocess the requests so that it runs in a reasonable amount of time.
            p = multiprocessing.Pool(len(d))
            rslt = list(p.map(dnsmapfunction, d))
            outfile.writelines(rslt)


#Mapping function
#Executes dig and returns formatted output.
def dnsmapfunction(ds):
    out = ""
    dnsrec = subprocess.getoutput("dig +nocmd +noall +answer +ttlid @{0} MX {1} ".format(ds, sys.argv[1]))
    dnsline = dnsrec.split('\n')
    for l in dnsline:
        temp = ""
        rslt = l.split()
        rslt.insert(0, ds)
        temp += ",".join(rslt) + "\n"
        out = out + temp
    print(out)
    return out

#ENTRY POINT
if __name__ == "__main__":
    main()
