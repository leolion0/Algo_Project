import csv
from prettytable import PrettyTable

# Stores a Request field 
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

# Accessor for all the requests
class RequestList:
    def __init__(self, inlist=[]):
        self.rList = inlist

    def __getitem__(self, key):
        return self.rList[key]

    # adds each request from the csv
    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)
        for row in tupList:
            id, vType, zip = row
            newVeh = Request(id, vType, zip)
            self.rList.append(newVeh)

    # Prints the request table
    def print(self):
        table = PrettyTable(['ID', 'Vehicle', 'Zip Code', 'Vehicle ID'])
        for request in self.rList:
           table.add_row([request.id, request.vType, request.zip, request.vehicle])
        print(table)

    # Prints the request table
    def __str__(self):
        table = PrettyTable(['ReqID', 'VehicleType', 'ZipCode', 'VehicleID', 'Distance'])
        for veh in self.rList:
           table.add_row([veh.id, veh.vType, veh.zip, veh.vehicle, veh.distance])
        return str(table)