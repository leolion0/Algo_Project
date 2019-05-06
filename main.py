import csv
import networkx as nx
import sys


class EmergencyVehicle:
    def __init__(self, id=-1, vType = -1, zip =-1):
        self.id = id
        self.vType = vType
        self.zip = zip

    def __str__(self):
        out = self.id + ", "
        out += str(self.vType) + ", "
        out += str(self.zip)
        return out


class EmergencyVehicleList:
    def __init__(self, inlist=[]):
        self.vList = inlist

    def __getitem__(self, key):
        return self.vList[key]

    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)
        for row in tupList:
            # print(row)
            id,vType,zip = row
            newVeh = EmergencyVehicle(id,vType,zip)
            self.vList.append(newVeh)

    def __str__(self):
        out = ''
        for veh in self.vList:
           out += str(veh) + '\n'
        return out


class Request:
    def __init__(self, id=-1, vType = -1, zip =-1):
        self.id = id
        self.vType = vType
        self.zip = zip

    def __str__(self):
        out = self.id + ", "
        out += str(self.vType) + ", "
        out += str(self.zip)
        return out


class RequestList:
    def __init__(self, inlist=[]):
        self.rList = inlist

    def __getitem__(self, key):
        return self.rList[key]

    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)
        for row in tupList:
            # print(row)
            id, vType, zip = row
            newVeh = Request(id, vType, zip)
            self.rList.append(newVeh)

    def __str__(self):
        out = ''
        for veh in self.rList:
            out += str(veh) + '\n'
        return out


class ZipDistance:
    def __init__(self, zip1 = -1, zip2 = -1, dist = -1):
        self.zip1 = zip1
        self.zip2 = zip2
        self.dist = dist

    def __str__(self):
        out = self.zip1 + ", "
        out += str(self.zip2) + ", "
        out += str(self.dist)
        return out


class ZipDistanceList:
    def __init__(self, inlist=[]):
        self.zList = inlist

    def __getitem__(self, key):
        return self.zList[key]

    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)
        for row in tupList:
            # print(row)
            zip1, zip2, dist = row
            newDist = ZipDistance(zip1, zip2, dist)
            self.zList.append(newDist)

    def __str__(self):
        out = ''
        for dist in self.zList:
            out += str(dist) + '\n'
        return out


class ZipGraph:
    def __init__(self):
        self.g = nx.Graph()
        pass

    def addDist(self, zipDist: ZipDistance):
        self.g.add_edge(zipDist.zip1, zipDist.zip2, weight=zipDist.dist)

    def constructFromZDList(self, zList: ZipDistanceList):
        for d in zList.zList:
            self.addDist(d)

    def dijkstras(self, startZip):
        nodes = set(self.g.nodes)
        distance = {}
        prev = {}
        for v in nodes:
            distance[v] = sys.maxsize
            prev[v] = None
        distance[startZip] = 0
        removed = set()
        while not nodes: #loop until no nodes are left
            u = min(distance, key=distance.get)
            removed.add(u)
            nodes.remove(u)

            neighbors = set()
            for v in iter(self.g[u]):
                neighbors.add(v)
            neighbors = neighbors - removed
            for v in neighbors:
                alt = distance[u] + self.g[u][v]['weight'] #might need to be casted to strings
                if alt < distance[v]:
                    distance[v] = alt
                    prev[v] = u
        return prev, distance










        pass


    def __str__(self):
        return str(self.g)




with open('EmergencyVehicles.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    theList = EmergencyVehicleList()
    theList.addAllFromCSV(reader)
    print(theList)

with open('Request.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    theList = RequestList()
    theList.addAllFromCSV(reader)
    print(theList)

with open('testDist.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    theList = ZipDistanceList()
    theList.addAllFromCSV(reader)
    g = ZipGraph()
    g.constructFromZDList(theList)

    # print(dict(g.g.nodes))


    # print(g.g.edges.data())

    print(g.dijkstras('001'))
