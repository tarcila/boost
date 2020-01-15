#!/usr/bin/env python

import json
from pprint import pprint
import urllib2
import hashlib

import networkx

with open("boost_libraries.json") as json_file:
    content = json.load(json_file)

version = content["version"]
libraries = content["libraries"]

for lib in libraries:
    name = lib["name"]
    uri = "https://github.com/boostorg/{name}/archive/boost-{version}.zip".format(name=name, version=version)
    print(uri)
    data = urllib2.urlopen(uri).read()
    m = hashlib.sha256()
    m.update(data)
    lib["sha256"] = m.hexdigest()


G = networkx.DiGraph()
G.add_nodes_from([x["name"] for x in libraries])

for lib in libraries:
    if "deps" in lib:
        f = lib["name"]
        for d in lib["deps"]:
            G.add_edge(d, f)

s = list(networkx.algorithms.lexicographical_topological_sort(G))
content["libraries"] = sorted(libraries, key = lambda k: s.index(k["name"]))

with open("boost_libraries.json", "wt") as json_file:
    json_file.write(json.dumps(content))