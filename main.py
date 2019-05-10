from classes.EmergencyVehicle import *
from classes.Request import *
from classes.ZipDistance import *
from classes.ZipGraph import *


vList = [] #Initialize lists for vehicles, requests, and zip distances respectively in wider scope.
rList = []
dList = []

#Constructs EmergencyVehicleList from csv file.
with open('EmergencyVehicles.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    vList = EmergencyVehicleList()
    vList.addAllFromCSV(reader)

#Same is done for requests and distances.
with open('Request.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rList = RequestList()
    rList.addAllFromCSV(reader)

with open('Distance.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dList = ZipDistanceList()
    dList.addAllFromCSV(reader)

#Create new ZipGraph and read in all edges (ZipDistances)
g = ZipGraph()
g.constructFromZDList(dList)

#Update vehicles at each zip node
g.updateVehicleLocations(vList)

#Print vehicles, requests, and distances as fed in from .csvs
print(vList)
print(rList)
print(dList)

print("\n\n------------------- Filling Requests -------------------\n\n")

#Do the thing
print(g.fillReqList(rList))
print("\n\nDone!")

