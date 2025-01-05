from datetime import datetime, timedelta

class Package:
    """
    Represents a package in the delivery system.
    """
    
    def __init__(self, id, address, city, state, zip_code, deadline, weight, special_notes="", status="At HUB"):
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
            special_notes: Any addition information about the package. Defaults to blank string.
        """
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = [[status,None]]
        self.special_notes = special_notes
    
    def __str__(self):
        """
        Return a string representation of the Package.

        Returns:
            A formatted string containing package ID and address details.
        """
        return f"Package {self.id}:\n" + \
                f"  {self.address}, {self.city}, {self.state} {self.zip_code}\n" + \
                f"  {self.weight} KG, Deadline: {self.deadline}" + \
                (len(self.special_notes) > 0 and f", Notes: {self.special_notes}\n" or "\n") + \
                '\n'.join([f"  {(x[1]) and (datetime.min + x[1]).strftime('%H:%M') or "??:??"}: {x[0]}" for x in self.status]) + "\n"
    
    def updateStatus(self, status, time=None):
        """
        Update the status of the package with timestamp.

        Args:
            status: New status of the package.
            time: Time of status update
        """
        self.status.append([status, time])
    
    def isOnTruck(self):
        return any(['Loaded on truck' in x[0] for x in self.status])

    def updateAddress(self, address, city, state, zip_code):
        """
        Update the address of the package.

        Args:
            address: New address of the package.
            city: New city of the package.
            state: New state of the package.
            zip_code: New ZIP code of the package.
        """
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
