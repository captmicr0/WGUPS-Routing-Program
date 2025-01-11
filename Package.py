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
        self.address_history = [[(self.address, self.city, self.state, self.zip_code), status_time]]
        self.deadline = deadline
        self.weight = weight
        self.status = [[status,status_time]]
        self.special_notes = special_notes
        self.expected_delivery = None
    
    def __str__(self, until=None):
        """
        Return a string representation of the Package.

        Args:
            until: Only print tracking history up to this time
        
        Returns:
            A formatted string containing package ID and address details.
        """
        address, city, state, zip_code = self.getAddress(until).split(",")
        trackingHistory = f"  Tracking History{f" until {(datetime.min + until).strftime("%I:%M %p")}" if until else ""}:\n"
        if until:
            trackingHistory += '\n'.join([f"    {(x[1]) and (datetime.min + x[1]).strftime("%I:%M %p") or "??:??"}: {x[0]}" for x in self.status if x[1] <= until])
        else:
            trackingHistory += '\n'.join([f"    {(x[1]) and (datetime.min + x[1]).strftime("%I:%M %p") or "??:??"}: {x[0]}" for x in self.status])
        return f"Package {self.id}:\n" + \
                f"  {address}, {city}, {state} {zip_code}\n" + \
                f"  {self.weight} KG, Deadline: {self.deadline and (datetime.min + self.deadline).strftime('%I:%M %p') or "EOD"}" + \
                (len(self.special_notes) > 0 and f", Notes: {self.special_notes}\n" or "\n") + \
                trackingHistory
    
    def __repr__(self):
        """
        Return a string representation of the Package object.

        This method provides a concise representation of the Package,
        which is useful for debugging and logging purposes.

        Returns:
            A string representation of the Package object, including its ID.
        """
        return f"Package(id={self.id})"
    
    def updateStatus(self, status, time=None):
        """
        Update the status of the package with timestamp.

        Args:
            status: New status of the package.
            time: Time of status update
        """
        #if [status, time] not in self.status:
        self.status.append([status, time])
    
    def isOnTruck(self, atTime=None):
        """
        Check if the package is currently loaded on a truck.

        Returns:
            Which truck the package is on, False is not loaded (or already delivered, accordin to atTime).
        """
        if atTime:
            alreadyLoaded = any(["Loaded on truck" in x[0] for x in self.status if x[1] < atTime])
            whichTruck = [x[0].split('#')[-1] for x in self.status if (x[1] < atTime) and ("Loaded on truck" in x[0])]
            alreadyDelivered = any(["Delivered" in x[0] for x in self.status if x[1] < atTime])
            return (alreadyLoaded and not alreadyDelivered) and int(whichTruck[0]) or False
        
        whichTruck = [x[0].split('#')[-1] for x in self.status if "Loaded on truck" in x[0]]
        return any(["Loaded on truck" in x[0] for x in self.status]) and int(whichTruck[0]) or False

    def isDelivered(self):
        """
        Check if the package has been delivered.

        Returns:
            True if the package is delivered, False otherwise.
        """
        #return "Delivered" in self.status[-1][0]
        return any(["Delivered" in x[0] for x in self.status])
    
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

    def updateAddress(self, address, city, state, zip_code, time=None):
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
        self.status.append(["Delivery address updated", time])
        self.address_history.append([(self.address, self.city, self.state, self.zip_code), time])
    
    def getAddress(self, time=None):
        if time is None or len(self.address_history) == 1:
            return ", ".join(map(str, self.address_history[-1][0])) if self.address_history else None

        for i in range(1, len(self.address_history)):
            previous_entry, previous_time = self.address_history[i - 1]
            current_entry, current_time = self.address_history[i]

            if previous_time <= time < current_time:
                return ", ".join(map(str, previous_entry))
        
        return ", ".join(map(str, self.address_history[-1][0])) if self.address_history else None
