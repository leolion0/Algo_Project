import csv
from prettytable import PrettyTable

#Contains fields for vehicle ID, vehicle type, and current location by zip
class EmergencyVehicle:
    def __init__(self, id=-1, vType = -1, zip =-1):
        self.id = id
        self.vType = vType
        self.zip = zip

#prints in same format as read from csv
    def __str__(self):
        out = self.id + ", "
        out += str(self.vType) + ", "
        out += str(self.zip)
        return out

#Class for list of emergency vehicles. Can be accessible by index if needed. Contains method for
#printing in a table format and reading in data from a csv file.
class EmergencyVehicleList:
    def __init__(self, inlist=[]):
        self.vList = inlist

    def __getitem__(self, key):
        return self.vList[key]

    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)

        for row in tupList:
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