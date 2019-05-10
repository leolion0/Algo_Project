import sys
import networkx as nx
from classes.Request import *
from queue import PriorityQueue
from classes.ZipDistance import *
from classes.EmergencyVehicle import *

#Where most of the magic happens. Utilizes a weighted, undirected graph from NetworkX
#as a structure for keeping track of distances. Maintains a dictionary of all vehicles
#at a given zip in the graph.

class ZipGraph:
    def __init__(self):
        self.g = nx.Graph()
        self.vehiclesByZip = {}
        pass

    #Adds weighted edge to the graph by passing in a ZipDistance object. Adds key to vehicles dictionary.
    def addDist(self, zipDist: ZipDistance):
        self.g.add_edge(zipDist.zip1, zipDist.zip2, weight=zipDist.dist)
        for e in self.g.nodes:
            self.vehiclesByZip.update({str(e):[]})

    #Constructs all the edges, weights, and vertices from a ZipDistanceList. Adds
    def constructFromZDList(self, zList: ZipDistanceList):
        for d in zList.zList:
            self.addDist(d)

    #Dijkstras algorithm utilizing priority queue to find the distances to all other nodes (zips) from the current node.
    #Returns dictionary in the form of zip:shortestPathFromStart
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
                alt = distance[u] + int(self.g[u][v]['weight'])
                if alt < distance[v]:
                    distance[v] = alt
                    pq.put((distance[v], v))
        return distance


    #Takes in an EmergencyVehicleList and adds those vehicles to the dictionary of locations in the
    #current ZipGraph instance.
    def updateVehicleLocations(self, elist: EmergencyVehicleList):
        for i in elist:
            try:
                zipList = self.vehiclesByZip[str(i.zip)]
            except:
                self.vehiclesByZip.update({str(i.zip):[]})
                zipList = self.vehiclesByZip[str(i.zip)]

            zipList.append(i)

            self.vehiclesByZip.update({str(i.zip):zipList})

    #Finds the closest vehicle of a requested type to a requested zip. Goes to nearest zip, sees if
    #vehicle type is there, then continues if not.
    def closestVehicle(self, startZip, vehicleType):
        dists = self.dijkstras(startZip)
        pq = PriorityQueue()
        for d in dists:
            pq.put((dists[d], d))
        while not pq.empty():
            u = pq.get()[1]
            for e in self.vehiclesByZip[str(u)]:
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

    #Takes a RequestList and processes each by calling fillReq()
    def fillReqList(self, reqL: RequestList):
        for r in reqL:
            r = self.fillReq(r)
        return reqL

    #Prints the graph of the Zips. Does not include vehicles at each zip.
    def __str__(self):
        return str(self.g)
