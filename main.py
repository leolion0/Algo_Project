import csv
import networkx as nx
import sys
import copy
from prettytable import PrettyTable


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

    def print(self):
        table = PrettyTable(['ID', 'Type', 'Zip Code'])
        for veh in self.vList:
           table.add_row([veh.id, veh.vType, veh.zip])
        print(table)

    def __str__(self):
        table = PrettyTable(['VehicleID', 'Type', 'ZipCode'])
        for v in self.vList:
           table.add_row([v.id, v.vType,v.zip])
        return str(table)


class Request:
    def __init__(self, id=-1, vType = -1, zip =-1, vehicleID = -1, distance = -1):
        self.id = id
        self.vType = vType
        self.zip = zip
        self.vehicle = vehicleID
        self.distance = distance

    def __str__(self):
        out = self.id + ", "
        out += str(self.vType) + ", "
        out += str(self.zip) + ", "
        out += str(self.vehicle) + ", "
        out += str(self.distance)
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

    def print(self):
        table = PrettyTable(['ID', 'Vehicle', 'Zip Code', 'Vehicle ID'])
        for request in self.rList:
           table.add_row([request.id, request.vType, request.zip, request.vehicle])
        print(table)

    def __str__(self):
        table = PrettyTable(['ReqID', 'VehicleType', 'ZipCode', 'VehicleID', 'Distance'])
        for veh in self.rList:
           table.add_row([veh.id, veh.vType, veh.zip, veh.vehicle, veh.distance])
        return str(table)


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
        table = PrettyTable(['Zip1', 'Zip2', 'Distance'])
        for z in self.zList:
           table.add_row([z.zip1, z.zip2, z.dist])
        return str(table)


class ZipGraph:
    def __init__(self):
        self.g = nx.Graph()
        self.vehiclesByZip = {}
        pass

    def addDist(self, zipDist: ZipDistance):
        self.g.add_edge(zipDist.zip1, zipDist.zip2, weight=zipDist.dist)

    def constructFromZDList(self, zList: ZipDistanceList):
        for d in zList.zList:
            self.addDist(d)
        for e in self.g.nodes:
            self.vehiclesByZip.update({str(e):[]})

    def dijkstras(self, startZip):
        nodes = set(self.g.nodes)
        distance = {}
        prev = {}
        for n in nodes:
            distance[n] = sys.maxsize
            prev[n] = None
        distance[startZip] = 0
        removed = set()
        while  len(nodes) > 0 : #loop until no nodes are left
            newDist = copy.deepcopy(distance)
            for i in removed:
                try:
                    newDist.pop(i)
                except:
                    pass
            u = min(newDist, key=newDist.get)
            removed.add(u)
            try:
                nodes.remove(u)
            except:
                pass

            neighbors = set()
            for v in iter(self.g[u]):
                neighbors.add(v)
            neighbors = neighbors - removed
            for z in neighbors:
                alt = distance[u] + int(self.g[u][z]['weight']) #might need to be casted to strings
                if alt < distance[z]:
                    distance[z] = alt
                    prev[z] = u
        return distance
    #Takes in the list created from the csv file and updates the vehicles zip code to its current location
    def updateVehicleLocations(self, elist: EmergencyVehicleList):
        for i in elist:
            # print(i.zip)
            try:
                zipList = self.vehiclesByZip[str(i.zip)]
            except:
                self.vehiclesByZip.update({str(i.zip):[]})
                zipList = self.vehiclesByZip[str(i.zip)]

            zipList.append(i)

            self.vehiclesByZip.update({str(i.zip):zipList})
            
    #Takes in the zip code( souce node) and vehicle type and finds the closet avaianle vehicle by calling the dijsktras function
    def closestVehicle(self, startZip, vehicleType):
        dists = self.dijkstras(startZip)
        while len(dists) > 0 :
            u = min(dists, key=dists.get)
            for e in  self.vehiclesByZip[str(u)]:
                if e.vType == str(vehicleType):
                    return e, dists[u]
            dists.pop(u)

    # Takes in request, finds closest available vehicle, updates request
    # vehicleID and distance, removes vehicle from ZipGraph(no double assignments)
    def fillReq(self, req: Request):
        closestV, distance = self.closestVehicle(req.zip, req.vType)
        req.distance = distance
        req.vehicle = closestV.id
        oldZipData = self.vehiclesByZip[closestV.zip]
        oldZipData.remove(closestV)
        self.vehiclesByZip[closestV.zip] = oldZipData
        return req

    def fillReqList(self, reqL: RequestList):
        for r in reqL:
            r = self.fillReq(r)
        return reqL

    def __str__(self):
        return str(self.g)

#Create lists for use when parsing the input from the csv files  
vList = []
rList = []
dList = []

with open('EmergencyVehicles.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    vList = EmergencyVehicleList()
    vList.addAllFromCSV(reader)
    # print(vList)

with open('Request.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rList = RequestList()
    rList.addAllFromCSV(reader)
    # print(rList)

with open('Distance.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dList = ZipDistanceList()
    dList.addAllFromCSV(reader)
    # print(dList)

g = ZipGraph()
g.constructFromZDList(dList)

# print(dict(g.g.nodes))
# print(g.g.edges.data())
g.updateVehicleLocations(vList)

print(vList)
print(rList)
print(dList)
print("\n\n------------------- Filling Requests -------------------\n\n")
print(g.fillReqList(rList))
print("\n\nDone!")
