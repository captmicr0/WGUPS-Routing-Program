class Driver:
    """
    Represents a driver in the delivery system.
    """
    def __init__(self, id, truck=None):
        """
        Initialize a Driver object.

        Args:
            id: Unique identifier for the driver.
            truck: The truck assigned to the driver. Defaults to None.
        """
        self.id = id
        self.truck = truck
    
    def assignTruck(self, truck):
        """
        Assign a truck to the driver.

        Args:
            truck: The truck to be assigned to the driver.

        Returns:
            Always returns True, indicating successful assignment.
        """
        truck.driver = self
        self.truck = truck
        return True
    
    def removeTruck(self):
        """
        Remove the assigned truck from the driver.

        This method removes the association between the driver and their assigned truck.
        """
        self.truck.driver = None
        self.truck = None
