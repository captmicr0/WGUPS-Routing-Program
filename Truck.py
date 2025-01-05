from datetime import datetime, timedelta

class Truck:
    """
    Represents a delivery truck in the package delivery system.
    """

    def __init__(self, id, start_time, speed=18, capacity=16):
        """
        Initialize a Truck object with given attributes.

        Args:
            id: Unique identifier for the truck.
            start_time: The time when the truck starts its route.
            speed: The speed of the truck in miles per hour. Defaults to 18.
            capacity: Maximum number of packages the truck can carry. Defaults to 16.
        """
        self.id = id
        self.packageIDs = []
        self.mileage = 0
        self.current_time = start_time
        self.speed = speed
        self.capacity = capacity
        self.current_location = "HUB"
        self.driver = None
    
    def __str__(self):
        """
        Return a string representation of the Driver.

        Returns:
            A string representation of the Driver.
        """
        return f"Truck #{self.id}, Assigned Driver: {self.driver.id}\n" + \
                f"  Speed {self.speed}, Capacity: {self.capacity}\n" + \
                f"  Mileage: {self.mileage}, Current Time: {(datetime.min + self.current_time).strftime("%H:%M")}\n"+ \
                f"  Location: {self.current_location}"
    
    def loadPackage(self, pkgHashTable, packageID):
        """
        Load a package onto the truck if there's available capacity.

        Args:
            pkgHashTable: The HashTable of packages
            packageID: The package ID to be loaded.

        Returns:
            True if the package was successfully loaded, False otherwise.
        """
        if len(self.packageIDs) < self.capacity:
            package = pkgHashTable.lookup(packageID)
            package.updateStatus("Loaded on truck", self.current_time)
            self.packageIDs.append(packageID)
            return True
        return False

    def updatePackagesStatus(self, pkgHashTable, status):
        """
        Update the status of all packages on the truck.

        Args:
            pkgHashTable: The HashTable of packages
            status: status update for all packages
        """
        for pkgID in self.packageIDs:
            package = pkgHashTable.lookup(pkgID)
            package.updateStatus(status, self.current_time)
    
    def deliverPackage(self, pkgHashTable, packageID, distance):
        """
        Deliver a package and update truck's status.

        Args:
            pkgHashTable: The HashTable of packages
            packageID: The package ID to be delivered.
            distance: The distance to the delivery location in miles.
        """
        package = pkgHashTable.lookup(packageID)
        travel_time = distance / self.speed
        self.current_time += timedelta(hours=travel_time)
        self.mileage += distance
        package.updateStatus("Delivered", self.current_time)
        self.packageIDs.remove(packageID)
        self.current_location = package.address

    def returnToHub(self, distance_to_hub):
        """
        Return truck to HUB

        Args:
            distance_to_hub: The distance to the delivery HUB in miles.
        """
        travel_time = distance_to_hub / self.speed
        self.current_time += timedelta(hours=travel_time)
        self.mileage += distance_to_hub
        self.current_location = "HUB"

    def getPackages(self, pkgHashTable):
        """
        Get a list of all Packages loaded on the truck.

        Args:
            pkgHashTable: The HashTable of packages
        """
        packages = []
        for pkgID in self.packageIDs:
            packages.append(pkgHashTable.lookup(pkgID))
        return packages

    def isFull(self):
        """
        Check if the truck is at capacity.
        
        Returns:
            True if the truck is at capacity, False otherwise.
        """
        return len(self.packageIDs) == self.capacity
