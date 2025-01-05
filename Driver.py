class Driver:
    """
    Represents a driver in the delivery system.
    """
    def __init__(self, id, availableTrucks=None):
        """
        Initialize a Driver object.

        Args:
            id: Unique identifier for the driver.
            availableTrucks: List of possible trucks the Driver can be assigned to. Defaults to None.
        """
        self.id = id
        self.truck = None
        if availableTrucks:
            self.assignTruck(availableTrucks)
    
    def __str__(self):
        """
        Return a string representation of the Driver.

        Returns:
            A string representation of the Driver.
        """
        return f"Driver #{self.id}, Assigned Truck #{self.truck.id}"
    
    def assignTruck(self, availableTrucks):
        """
        Assign a truck to the driver.

        Args:
            availableTrucks: List of possible trucks the Driver can be assigned to.

        Returns:
            True if assignment successful, False otherwise.
        """
        for truck in availableTrucks:
            if truck.driver is None:
                truck.driver = self
                self.truck = truck
                return True
        return False
    
    def removeTruck(self):
        """
        Remove the assigned truck from the driver.

        This method removes the association between the driver and their assigned truck.
        """
        self.truck.driver = None
        self.truck = None
