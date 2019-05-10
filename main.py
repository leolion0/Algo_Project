from classes.Graph import *
from classes.Request import *
from classes.ZipGraph import *
from classes.ZipDistance import *
from classes.EmergencyVehicle import *

#Initialize lists for vehicles, requests, and zip distances respectively in wider scope.
vList = [] 
rList = []
dList = []

#Constructs EmergencyVehicleList from csv file.
with open('EmergencyVehicles.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    vList = EmergencyVehicleList()
    vList.addAllFromCSV(reader)

# Create Request List
with open('Request.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rList = RequestList()
    rList.addAllFromCSV(reader)

# Create Zip Distance List
with open('Distance.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dList = ZipDistanceList()
    dList.addAllFromCSV(reader)

#Create new ZipGraph and read in all edges (ZipDistances)
g = ZipGraph()
g.constructFromZDList(dList)
g.updateVehicleLocations(vList)

# User output of working systems
print(vList)
print(rList)
print(dList)

print("\n\n------------------- Filling Requests -------------------\n\n")

#Do the thing
print(g.fillReqList(rList))
print("\n\nDone!")

