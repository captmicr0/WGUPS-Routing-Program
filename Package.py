import re
from datetime import datetime, timedelta

class Package:
    """
    Represents a package in the delivery system.
    """
    
    def __init__(self, id, address, city, state, zip_code, deadline, weight, special_notes="", status="At HUB", status_time=timedelta(hours=7, minutes=00)):
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
            special_notes: Any addition information about the package. Defaults to blank string.
            status: Current status of the package. Defaults to "At HUB".
            status_time: Current status time. Defaults to 7:00 AM.
        """
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = [[status,status_time]]
        self.special_notes = special_notes
    
    def __str__(self):
        """
        Return a string representation of the Package.

        Returns:
            A formatted string containing package ID and address details.
        """
        return f"Package {self.id}:\n" + \
                f"  {self.address}, {self.city}, {self.state} {self.zip_code}\n" + \
                f"  {self.weight} KG, Deadline: {self.deadline and (datetime.min + self.deadline).strftime('%H:%M') or "EOD"}" + \
                (len(self.special_notes) > 0 and f", Notes: {self.special_notes}\n" or "\n") + \
                f"  Tracking History:\n" + \
                '\n'.join([f"    {(x[1]) and (datetime.min + x[1]).strftime("%H:%M") or "??:??"}: {x[0]}" for x in self.status])
    
    def __repr__(self):
        return f"Package(id={self.id})"
    
    def updateStatus(self, status, time=None):
        """
        Update the status of the package with timestamp.

        Args:
            status: New status of the package.
            time: Time of status update
        """
        self.status.append([status, time])
    
    def isOnTruck(self):
        """
        Check if the package is currently loaded on a truck.

        Returns:
            True if the package is on a truck, False otherwise.
        """
        return any(["Loaded on truck" in x[0] for x in self.status])

    def isDelivered(self):
        """
        Check if the package has been delivered.

        Returns:
            True if the package is delivered, False otherwise.
        """
        return "Delivered" in self.status[-1][0]
    
    def getRequiredTruckID(self):
        """
        Get the required truck ID for the package, if specified in special notes.

        Returns:
            The required truck ID, or None if not specified.
        """
        notes = self.special_notes
        if "Can only be on truck" in notes:
            return int(notes.split()[-1])
        return None

    def getArrivalTime(self):
        """
        Get the arrival time of the package at the depot, if delayed.

        Returns:
            The arrival time as a timedelta object, or None if not delayed.
        """
        notes = self.special_notes
        # Handle delayed packages
        if "Delayed on flight---will not arrive to depot until" in notes:
            time = re.search(r"([0-9]{1,2})\:([0-9]{2})", notes)
            return timedelta(hours=int(time.group(1)), minutes=int(time.group(2)))
        # Handle wrong address packages
        if "Wrong address listed" in notes:
            # Assume correct addresses are known by 10:20 AM
            return timedelta(hours=10, minutes=20)
        return None

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
