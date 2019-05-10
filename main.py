from classes.EmergencyVehicle import *
from classes.Request import *
from classes.ZipDistance import *
from classes.ZipGraph import *


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
