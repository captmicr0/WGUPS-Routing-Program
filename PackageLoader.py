from datetime import datetime, timedelta

from Driver import Driver
from Truck import Truck

from HashTable import HashTable
from Package import Package

class PackageLoader:
    def __init__(self, trucks, pkgHashTable):
        """
        Initialize a PackageLoader object with given attributes.

        Args:
            trucks: Avaiable Trucks to load packages onto
            pkgHashTable: The hashTable containing all packages.
        """
        self.trucks = trucks
        self.pkgHashTable = pkgHashTable
        self.pkgDependencies = self._getPackageDependencies()
    
    def _getPackageDependencies(self):
        """
        Get list of all packages that must be delivered together

        Returns:
            A list of package list that must be delivered together
        """
        masterList = []

        for bucket in self.pkgHashTable.table:
            for _, pkg in bucket:
                if pkg and "Must be delivered with" in pkg.special_notes:
                    # Get list of packages that must be delivered with the current package
                    pkgDependencies = self._getPackageSubDependencies(pkg)

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

    def _getPackageSubDependencies(self, package):
        """
        Parse packages special notes and get a list of directly related packages

        Args:
            package: The initial package
        
        Returns:
            A list of packages that must be delivered with the initial package
        """
        notes = package.special_notes

        if "Must be delivered with" in notes:
            pkgDependencies = [package]

            # Get IDs of other packages that must be delivered with the given package
            IDs = [int(x) for x in notes.replace(',',' ').split() if x.isdigit()]

            # Append IDs aof additional packages that must be delivered with above packages
            for pkgID in IDs:
                pkg = self.pkgHashTable.lookup(pkgID)
                pkgDependencies.append(pkg)
                additionalPkgs = self._getPackageSubDependencies(pkg)
                if additionalPkgs is not None:
                    pkgDependencies.extend(additionalPkgs)

            return pkgDependencies
