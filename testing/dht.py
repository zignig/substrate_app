#!/usr/bin/python -i

from pydht import DHT 

host,port = '10.251.10.224',7000
strap = 'bl3dr.com'
d = DHT(host,port,boot_host=strap,boot_port=port)
nodes = d.iterative_find_nodes(2)
print nodes
server = d['server']
print server
import requests
r = requests.get(server)
print r.json()

