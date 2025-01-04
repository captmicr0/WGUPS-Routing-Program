class Package:
    """
    Represents a package in the delivery system.
    """
    
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status="At HUB", note=""):
        """
        Initialize a Package object with given attributes.

        Args:
            id: Unique identifier for the package.
            address: Delivery address.
            city: Destination city.
            state: Destination state.
            zip_code: Destination ZIP code.
            deadline: Delivery deadline.
            weight: Weight of the package.
            status: Current status of the package. Defaults to "At HUB".
            note: Any addition information about the package. Defaults to blank string.
        """
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None
        self.note = note
    
    def __str__(self):
        """
        Return a string representation of the Package.

        Returns:
            A formatted string containing package ID and address details.
        """
        return f"Package {self.id}: {self.address}, {self.city}, {self.state} {self.zip_code} ({self.note})"
    
    def update_status(self, status, time=None):
        """
        Update the status of the package and set delivery time if delivered.

        Args:
            status: New status of the package.
            time: Time of delivery, required if status is "Delivered".
        """
        self.status = status
        if status == "Delivered":
            self.delivery_time = time
