import sys
import networkx as nx
from queue import PriorityQueue
from prettytable import PrettyTable

from classes.Request import *
from classes.ZipDistance import *
from classes.EmergencyVehicle import *

class ZipGraph:
    def __init__(self):
        self.g = nx.Graph()
        self.vehiclesByZip = {}
        pass

    # Adds the edge between two zips
    def addDist(self, zipDist: ZipDistance):
        self.g.add_edge(zipDist.zip1, zipDist.zip2, weight=zipDist.dist)

    # Build the Graph from the Ziplist
    def constructFromZDList(self, zList: ZipDistanceList):
        for d in zList.zList:
            self.addDist(d)
        for e in self.g.nodes:
            self.vehiclesByZip.update({str(e):[]})

    # Implements dijktras algorithm with a prority queue
    # Finds the list of distances from startZip to all other zips
    def dijkstras(self, startZip):
        pq = PriorityQueue()
        distance = {}
        for n in self.g.nodes:
            distance[n] = sys.maxsize
        pq.put((0, startZip))
        distance[startZip] = 0

        while not pq.empty():  #loop until no nodes are left
            u = pq.get()[1]
            for v in iter(self.g[u]):
                alt = distance[u] + int(self.g[u][v]['weight']) #might need to be casted to strings
                if alt < distance[v]:
                    distance[v] = alt
                    pq.put((distance[v], v))
        return distance

    # Update Vehicles to new location unless already there
    def updateVehicleLocations(self, elist: EmergencyVehicleList):
        for vehicle in elist:
            try:
                zipList = self.vehiclesByZip[str(vehicle.zip)]
            except:
                self.vehiclesByZip.update({str(vehicle.zip):[]})
                zipList = self.vehiclesByZip[str(vehicle.zip)]

            zipList.append(vehicle)

            self.vehiclesByZip.update({str(vehicle.zip):zipList})

    # Find closest vehicle via dijkstras algorithm
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

    # Given all requests it fufills them
    def fillReqList(self, reqL: RequestList):
        for r in reqL:
            r = self.fillReq(r)
        return reqL

    def __str__(self):
        return str(self.g)
