import csv
from prettytable import PrettyTable

# Stores the distance between two zips 
class ZipDistance:
    def __init__(self, zip1 = -1, zip2 = -1, dist = -1):
        self.zip1 = zip1
        self.zip2 = zip2
        self.dist = dist

    def __str__(self):
        out = self.zip1 + ", "
        out += str(self.zip2) + ", "
        out += str(self.dist)
        return out

# Accessor for all the zip nodes
class ZipDistanceList:
    def __init__(self, inlist=[]):
        self.zList = inlist

    def __getitem__(self, key):
        return self.zList[key]

    # Adds each Zip Distance from the csv
    def addAllFromCSV(self, reader: csv.reader):
        tupList = list(reader)
        for row in tupList:
            # print(row)
            zip1, zip2, dist = row
            newDist = ZipDistance(zip1, zip2, dist)
            self.zList.append(newDist)

    # Prints the Zip distance table
    def __str__(self):
        table = PrettyTable(['Zip1', 'Zip2', 'Distance'])
        for z in self.zList:
           table.add_row([z.zip1, z.zip2, z.dist])
        return str(table)