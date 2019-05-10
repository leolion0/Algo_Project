import sys
import networkx as nx
from classes.Request import *
from queue import PriorityQueue
from classes.ZipDistance import *
from prettytable import PrettyTable
from classes.EmergencyVehicle import *

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
