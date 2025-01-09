# Ryan V, Student ID# 012201560

from datetime import datetime, timedelta

from PackageImporter import PackageImporter
from AddressImporter import AddressImporter

from Driver import Driver
from Truck import Truck

from HashTable import HashTable
from Package import Package

from Routing import Routing

from InfoUI import InfoUI

# Number of Trucks and Drivers in the delivery system
NUM_TRUCKS = 3
NUM_DRIVERS = 2
NUM_MIN = min(NUM_TRUCKS, NUM_DRIVERS) # Since Drivers stay with their assigned Truck, extras are not used

# Import addresses and distances from the csv file
addressImporter = AddressImporter('distances.csv')

# Import Packages from the csv file and insert them into the HashTable
pkgImporter = PackageImporter('packages.csv')
pkgHashTable = HashTable(10)

for pkg in pkgImporter.getPackages():
    pkgHashTable.insert(pkg)

# Create Routing instance
# This handles package dependencies and other special cases
# Uses the NN sorting algorithm to deliver packages
router = Routing(addressImporter, pkgHashTable)

# Initialize Trucks and Drivers
# Assume 08:00 AM is when trucks start their routes
trucks = [Truck(id, timedelta(hours=8, minutes=0)) for id in range(1, NUM_MIN + 1)]
drivers = [Driver(id, trucks) for id in range(1, NUM_MIN + 1)]

# Get the earliest delayed arrival time
delayedArrivalTime = timedelta(hours=24, minutes=0)

for pkg in pkgHashTable:
    pkgArrivalTime = pkg.getArrivalTime()
    if pkgArrivalTime and (delayedArrivalTime > pkgArrivalTime):
        delayedArrivalTime = pkgArrivalTime

# Load packages onto trucks, initial start-of-day load
for truck in trucks:
    router.loadPackagesOntoTruck(truck)

# Deliver packages
# This will load more packages onto the trucks as needed
router.deliverPackages(trucks)

# Creates InfoUI instance and starts the UI menu loop
ui = InfoUI(pkgHashTable, trucks)
#ui.mainMenuLoop()
