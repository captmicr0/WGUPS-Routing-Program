# Ryan V, Student ID# 012201560

from datetime import datetime, timedelta

from PackageImporter import PackageImporter
from AddressImporter import AddressImporter

from Driver import Driver
from Truck import Truck

from HashTable import HashTable
from Package import Package

# Number of Trucks and Drivers in the delivery system
NUM_TRUCKS = 3
NUM_DRIVERS = 2

# Initialize Trucks and Drivers
NUM_MIN = min(NUM_TRUCKS, NUM_DRIVERS) # Since Drivers stay with their assigned Truck, extras are not used
trucks = [Truck(id, timedelta(hours=8, minutes=0, seconds=0)) for id in range(1, NUM_MIN + 1)]
drivers = [Driver(id, trucks) for id in range(1, NUM_MIN + 1)]
print(trucks[0])
# Import Packages from the csv file and insert them into the HashTable
pkgImporter = PackageImporter('packages.csv')
pkgHashTable = HashTable(len(pkgImporter.getPackages()))

for pkg in pkgImporter.getPackages():
    pkgHashTable.insert(pkg)

def getAssociatedPackages():
    """
    Get list of all packages that must be delivered together

    Args:
        package: The initial package
    
    Returns:
        A list of packages that must be delivered together
    """
    pass

def getPackageDependencies(package):
    """
    Parse packages special notes and get a list of directly related packages

    Args:
        package: The initial package
    
    Returns:
        A list of directly related packages that must be delivered together
    """
    notes = package.special_notes

    if "Must be delivered with" in notes:
        pkgDependencies = [package]

        # Get IDs of other packages that must be delivered with the given package
        IDs = [int(x) for x in notes.replace(',',' ').split() if x.isdigit()]

        # Append IDs aof additional packages that must be delivered with above packages
        for pkgID in IDs:
            pkg = pkgHashTable.lookup(pkgID)
            pkgDependencies.append(pkg)
            additionalPkgs = getPackageDependencies(pkg)
            if additionalPkgs is not None:
                pkgDependencies.extend(additionalPkgs)

        return pkgDependencies

def getRequiredTruckID(self, pkgID):
    notes = pkgHashTable.lookup(pkgID).special_notes
    if "Can only be on truck" in notes:
        return int(notes.split()[-1])
    return None

