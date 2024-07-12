from shodan import Shodan

import json

def shodan_org_scan(query, apiKey):
    api = Shodan(apiKey)
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