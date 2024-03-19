from langchain.tools import tool
from shodan import Shodan

import json

api = Shodan('put your own API KEY HERE i have redacted mine')

@tool
def shodan_ip_lookup(query: str) -> str:
    """Perform a quick scan on an IP using the Shodan API"""
    if ("query" in query):
        if "'" in query:
            query = query.replace("'", '"')
        x = query.split('"')
        y = str(api.host(x[1], minify=True, history=False))
    else:
        y = str(api.host(query, minify=True, history=False))
    return y

@tool
def shodan_search(query: str) -> str:
    """Search for services or hosts using the Shodan API."""
    if ("query" in query):
        if "'" in query:
            query = query.replace("'", '"')
        x = query.split('"')
        result = api.search(x)
    else:
        result = api.search(query)

    z = 0
    totalResults = ''
    for service in result['matches']:
        z += 1
        hostnameList = []
        for hostnames in service['hostnames']:
            hostnameList.append(hostnames)
        totalResults += '{0}. Oranization: {1}, IP: {2}, Hostnames: {3}, Port: {4}.\n'.format(z, service['org'], service['ip_str'], hostnameList, service['port'])
    return totalResults

#print(shodan_search('google'))

@tool
def shodan_org_scan(query: str) -> str:
    """Get a list of running services and ports by running a scan on a company using the Shodan API"""
    #print("Getting info, please wait...")
    if ("query" in query):
        if "'" in query:
            query = query.replace("'", '"')
        x = query.split('"')
        result = api.search(x)
    else:
        result = api.search(query)

    report = ''
    ipList = []
    #listCount = 1
    for service in result['matches']:
        host = api.host(service['ip_str'], minify=True, history=False)
        openPorts = []
        for port in host['ports']:
            openPorts.append(port)
        hostnameList = []
        for hostname in host['hostnames']:
            hostnameList.append(hostname)
        report += '\nIP: {0}, Hostnames: {1}, Ports: {2}, Operating System: {3}.'.format(service['ip_str'], hostnameList, openPorts, host['os'])
        #listCount = listCount + 1
    report = report.replace('None.', 'Unknown.')
    return report

#print(shodan_org_scan('company name'))
