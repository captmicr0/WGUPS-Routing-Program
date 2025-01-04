from datetime import timedelta

class Truck:
    """
    Represents a delivery truck in the package delivery system.
    """

    def __init__(self, id, start_time, speed=18, capacity=16):
        """
        Initialize a Truck object with given attributes.

        Args:
            id Unique identifier for the truck.
            start_time: The time when the truck starts its route.
            speed: The speed of the truck in miles per hour. Defaults to 18.
            capacity: Maximum number of packages the truck can carry. Defaults to 16.
        """
        self.id = id
        self.packages = []
        self.mileage = 0
        self.current_time = start_time
        self.speed = speed
        self.capacity = capacity
        self.current_location = "HUB"
    
    def loadPackage(self, package):
        """
        Load a package onto the truck if there's available capacity.

        Args:
            package (Package): The package to be loaded.

        Returns:
            True if the package was successfully loaded, False otherwise.
        """
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            return True
        return False
    
    def deliverPackage(self, package, distance):
        """
        Deliver a package and update truck's status.

        Args:
            package: The package to be delivered.
            distance: The distance to the delivery location in miles.
        """
        travel_time = distance / self.speed
        self.current_time += timedelta(hours=travel_time)
        self.mileage += distance
        package.update_status("Delivered", self.current_time)
        self.package.remove(package)
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
