class Routing:
    """
    An implementation to sort and load packages onto trucks.
    Handles special cases such as combined delivery, delays, and wrong addresses.
    """

    def __init__(self, addressImporter, pkgHashTable):
        """
        Initialize a Routing object with given attributes.

        Args:
            trucks: Avaiable Trucks to load packages onto
            pkgHashTable: The hashTable containing all packages.
        """
        self.addressImporter = addressImporter
        self.pkgHashTable = pkgHashTable
        self.pkgDependencies = self._getPackageDependencies()
    
    def deliverPackages(self, trucks):
        # Loop until all packages are delivered
        while not self._allPackagesDelivered():
            # Deliver packages for each truck
            for truck in trucks:
                current_address = "HUB"

                # Update status of all packages loaded on truck to "En route"
                truck.updatePackagesStatus(self.pkgHashTable, "En route")

                # Deliver all packages
                while len(truck.packageIDs) > 0:
                    # Get first item in packageID list
                    # Note: When a package is delivered, it's removed from the list
                    pkgID = truck.packageIDs[0]
                    pkg = self.pkgHashTable.lookup(pkgID)

                    # Get the distance between the current address and delivery address
                    distance = self.addressImporter.distance(current_address, pkg.address)

                    # Delivery the package
                    truck.deliverPackage(self.pkgHashTable, pkgID, distance)

                    # Update the current address
                    current_address = pkg.address

                # Return to HUB
                distance = self.addressImporter.distance(current_address, "HUB")
                truck.returnToHub(distance)
            
            # If any packages remain, load them onto the truck
            for truck in trucks:
                self.loadPackagesOntoTruck(truck)
    
    def _allPackagesDelivered(self):
        return all([pkg.isDelivered() for bucket in self.pkgHashTable.table for _, pkg in bucket])
    
    def loadPackagesOntoTruck(self, truck):
        """
        Load packages onto the given truck.

        Args:
            truck: The truck to load packages onto.
        """
        # Load packages until the Truck is at capacity
        loadablePkgs = self._getLoadablePackages(truck)
        while (truck.current_location == "HUB") and (len(loadablePkgs) > 0) and (not truck.isFull()):
            address = None

            # Set address to HUB if truck is empty
            if len(truck.packageIDs) == 0:
                address = "HUB"
            else:
                lastPkg = self.pkgHashTable.lookup(truck.packageIDs[-1])
                address = lastPkg.address

            # Load the closest package to the previous address
            nearestPkg = self._findClosestPackage(address, loadablePkgs)
            truck.loadPackage(self.pkgHashTable, nearestPkg.id)

            # If package ID is 9, update address
            # This will only happen when the truck is able to load the package,
            # after 10:20 AM when the correect address is known
            if nearestPkg.id == 9:
                nearestPkg.updateAddress("410 S State St", "Salt Lake City", "UT", 84111)
                # Resort, since the route will change due to the new address
                self._resortTruckPacakges(truck)
            
            # Check for any dependent packages and load them
            for subList in self.pkgDependencies:
                if nearestPkg in subList:
                    for dependentPkg in subList:
                        if not dependentPkg.isOnTruck():
                            truck.loadPackage(self.pkgHashTable, dependentPkg.id)
                    # Resort, since the dependent packages were not added in a sorted manner
                    self._resortTruckPacakges(truck)
    
    def _resortTruckPacakges(self, truck):
        """
        Resort packages on the truck based on nearest neighbor algorithm.

        Args:
            truck: The truck whose packages need to be resorted.
        """
        sortedIDs = []
        current_address = "HUB"
        packages = [self.pkgHashTable.lookup(id) for id in truck.packageIDs]

        while len(packages) > 0:
            nnPackage = self._findClosestPackage(current_address, packages)
            sortedIDs.append(nnPackage.id)
            current_address = nnPackage.address
            packages.remove(nnPackage)
        
        truck.packageIDs = sortedIDs

    def _findClosestPackage(self, current_address, packages):
        """
        Find the closest package to the current address.

        Args:
            current_address: The current address to compare against.
            packages: List of packages to search through.

        Returns:
            The package closest to the current address.
        """

        if not packages:
            return None

        # Uses Python's built-in min function with a key parameter to find the package with the minimum distance.
        return min(
            packages,
            key=lambda pkg: self.addressImporter.distance(pkg.address, current_address)
        )

    def _getLoadablePackages(self, truck):
        """
        Get all packages that are able to be loaded onto the given truck

        Args:
            truck: Truck to load packages onto
        
        Returns:
            A list of package list that can be loaded onto the truck
        """
        unloadablePkgs = self._getUnloadablePackages(truck)
        
        return [pkg for pkg in self._getUnloadedPackages() if pkg not in unloadablePkgs]

    def _getUnloadedPackages(self):
        """
        Get all packages that are NOT loaded onto a truck
        
        Returns:
            A list of packages that are NOT loaded onto a truck
        """
        return [pkg for bucket in self.pkgHashTable.table for _, pkg in bucket if not pkg.isOnTruck()]

    def _getUnloadablePackages(self, truck):
        """
        Get all packages that are NOT able to be loaded onto the given truck

        Args:
            truck: Truck to load packages onto
        
        Returns:
            A list of package list that can NOT be loaded onto the truck
        """
        unloadablePkgs = []
        
        for bucket in self.pkgHashTable.table:
            for _, pkg in bucket:
                # If the package is already loaded onto a truck, add it to the list
                if pkg.isOnTruck():
                    unloadablePkgs.append(pkg)
                
                # Handle delayed packages
                elif (pkg.getRequiredTruckID() is not None) and (pkg.getRequiredTruckID() != truck.id):
                    if pkg not in unloadablePkgs:
                        unloadablePkgs.append(pkg)
                
                # Handle packages that need to be on a specific truck
                elif (pkg.getArrivalTime() is not None) and (pkg.getArrivalTime() >= truck.current_time):
                    unloadablePkgs.append(pkg)

                    # Make sure any dependent packages are unloadable aswell
                    for subList in self.pkgDependencies:
                        # Does the package have an dependencies?
                        if pkg in subList:
                            # Add all of them to the unloadable list if they aren't already
                            for dependentPkg in subList:
                                if dependentPkg not in unloadablePkgs:
                                    unloadablePkgs.append(dependentPkg)
        
        return unloadablePkgs
    
    def _getPackageDependencies(self):
        """
        Get list of all packages that must be delivered together.

        Returns:
            A list of package lists that must be delivered together.
        """
        masterList = []
        for bucket in self.pkgHashTable.table:
            for _, pkg in bucket:
                if pkg and "Must be delivered with" in pkg.special_notes:
                    pkgDependencies = self._getPackageSubDependencies(pkg)
                    self._updateMasterList(masterList, pkgDependencies)
        return masterList

    def _getPackageSubDependencies(self, package):
        """
        Parse package's special notes and get a list of directly related packages.

        Args:
            package: The initial package.

        Returns:
            A list of packages that must be delivered with the initial package.
        """
        notes = package.special_notes
        if "Must be delivered with" in notes:
            pkgDependencies = [package]
            IDs = [int(x) for x in notes.replace(',', ' ').split() if x.isdigit()]
            for pkgID in IDs:
                pkg = self.pkgHashTable.lookup(pkgID)
                pkgDependencies.append(pkg)
                additionalPkgs = self._getPackageSubDependencies(pkg)
                if additionalPkgs is not None:
                    pkgDependencies.extend(additionalPkgs)
            return pkgDependencies

    def _updateMasterList(self, masterList, pkgDependencies):
        """
        Update the master list of package dependencies.

        Args:
            masterList: The current master list of package dependencies.
            pkgDependencies: New package dependencies to be added or merged.
        """
        combineList = next((subList for subList in masterList if any(dep in subList for dep in pkgDependencies)), None)
        if combineList:
            combineList.extend([dep for dep in pkgDependencies if dep not in combineList])
        else:
            masterList.append(pkgDependencies)
