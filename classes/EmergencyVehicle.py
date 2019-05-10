import csv
from prettytable import PrettyTable

# A single emergency vehicle
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

# An accessor for all the emergency vehicles
class EmergencyVehicleList:
    def __init__(self, inlist=[]):
        self.vList = inlist

    def __getitem__(self, key):
        return self.vList[key]

    # Reads csv file and adds each row
    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)

        for row in tupList:
            # print(row)
            id,vType,zip = row
            newVeh = EmergencyVehicle(id,vType,zip)
            self.vList.append(newVeh)

    # Prints the table of vehicles
    def print(self):
        table = PrettyTable(['ID', 'Type', 'Zip Code'])
        for veh in self.vList:
           table.add_row([veh.id, veh.vType, veh.zip])
        print(table)

    # Prints the table of vehicles
    def __str__(self):
        table = PrettyTable(['VehicleID', 'Type', 'ZipCode'])
        for v in self.vList:
           table.add_row([v.id, v.vType,v.zip])
        return str(table)