# Ryan V, Student ID# 012201560

from datetime import datetime, timedelta

from PackageImporter import PackageImporter
from AddressImporter import AddressImporter

from Driver import Driver
from Truck import Truck

from HashTable import HashTable
from Package import Package

from pprint import pprint

# Number of Trucks and Drivers in the delivery system
NUM_TRUCKS = 3
NUM_DRIVERS = 2
NUM_MIN = min(NUM_TRUCKS, NUM_DRIVERS) # Since Drivers stay with their assigned Truck, extras are not used

# Initialize Trucks and Drivers
trucks = [Truck(id, timedelta(hours=8, minutes=0, seconds=0)) for id in range(1, NUM_MIN + 1)]
drivers = [Driver(id, trucks) for id in range(1, NUM_MIN + 1)]

# Import Packages from the csv file and insert them into the HashTable
pkgImporter = PackageImporter('packages.csv')
pkgHashTable = HashTable(10)

for pkg in pkgImporter.getPackages():
    pkgHashTable.insert(pkg)

def getAssociatedPackages():
    """
    Get list of all packages that must be delivered together

    Args:
        package: The initial package
    
    Returns:
        A list of package list that must be delivered together
    """
    masterList = []

    for bucket in pkgHashTable.table:
        for _, pkg in bucket:
            if pkg and "Must be delivered with" in pkg.special_notes:
                # Get list of packages that must be delivered with the current package
                pkgDependencies = getPackageDependencies(pkg)

                combineList = None

                # Check if any of those packages are already in an list 
                for dependency in pkgDependencies:
                    for idx, subList in enumerate(masterList):
                        if dependency in subList:
                            combineList = subList
                            break

                # If any package is already in a list, append all dependencies to that list
                if combineList:
                    for dependency in pkgDependencies:
                        if dependency not in combineList:
                            combineList.append(dependency)
                # Otherwise, add all dependencies to a new list
                else:
                    masterList.append(pkgDependencies)
    
    return masterList

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
