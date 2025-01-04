import csv, re

import HashTable, Truck, Package

def ImportPackageFile(file):
    packages = []
    with open(file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            pkg = Package(
                row['PackageID'],
                row['Address'],
                row['City'],
                row['State'],
                row['Zip'],
                row['DeliveryDeadline'],
                row['WeightKILO'],
                row['SpecialNotes'])
            packages.append(pkg)

def ImportDistanceFile(file):
    addresses = []
    distances = []
    with open(file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            number, street, zipcode = re.findall(
                r"([0-9]+)\s+(.*?)\(([0-9]{5})\)",
                row[1])[0]
            