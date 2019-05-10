from classes.EmergencyVehicle import *
from classes.Request import *
from classes.ZipDistance import *
from classes.ZipGraph import *

vList = []
rList = []
dList = []

# Create Emergency Vehicle List
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

g = ZipGraph()
g.constructFromZDList(dList)
g.updateVehicleLocations(vList)

# User output of working systems
print(vList)
print(rList)
print(dList)
print("\n\n------------------- Filling Requests -------------------\n\n")
print(g.fillReqList(rList))
print("\n\nDone!")
