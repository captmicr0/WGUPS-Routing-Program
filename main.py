# Ryan V, Student ID# 012201560

from datetime import datetime, timedelta

from PackageImporter import PackageImporter
from AddressImporter import AddressImporter

from Driver import Driver
from Truck import Truck

from HashTable import HashTable
from Package import Package

from SortingLoader import SortingLoader

# Number of Trucks and Drivers in the delivery system
NUM_TRUCKS = 3
NUM_DRIVERS = 2
NUM_MIN = min(NUM_TRUCKS, NUM_DRIVERS) # Since Drivers stay with their assigned Truck, extras are not used

# Initialize Trucks and Drivers
trucks = [Truck(id, timedelta(hours=8, minutes=0, seconds=0)) for id in range(1, NUM_MIN + 1)]
drivers = [Driver(id, trucks) for id in range(1, NUM_MIN + 1)]

# Import addresses and distances from the csv file
addressImporter = AddressImporter('distances.csv')

# Import Packages from the csv file and insert them into the HashTable
pkgImporter = PackageImporter('packages.csv')
pkgHashTable = HashTable(10)

for pkg in pkgImporter.getPackages():
    pkgHashTable.insert(pkg)

# Create SortingLoader instance
sortingLoader = SortingLoader(addressImporter, pkgHashTable)

print(sortingLoader.pkgDependencies)