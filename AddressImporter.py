import csv, re

class AddressImporter:
    """
    A class for importing address data and distances from a CSV file.
    """
    def __init__(self, file):
        """
        Initialize the AddressImporter with the given CSV file and process its contents.

        Args:
            file: Path to the CSV file containing address and distance data.
        """
        self.file = file
        self.count = 0  # Counter for the number of addresses
        self.addr_names = [] # List to store address names/titles
        self.addresses = [] # List to store formatted addresses
        self.distances = [] # 2D list to store distances between addresses
        self._import_addresses() # Import address data
        self._import_distances() # Import distance data
    
    def _import_addresses(self):
        """
        Private method to import address data from the CSV file.
        """
        # Regex pattern to match the name/title of the address
        # Group 1: Name/title of the address
        name_pattern = r"^[\s\S]*?(.*?)$"
        # Group 1: Name/title of the address
        # Group 1: Number
        # Group 2: Street
        # Group 3: Zipcode
        addr_pattern = r"^\s*(\d+)\s+(.*)\s*\((\d{5})\)\s*$"

        with open(self.file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Add address name to list
                name_match = re.search(name_pattern, row[0], re.MULTILINE)
                self.addr_names.append(name_match.group(1))
                # Add formatted address to list
                addr_match = re.search(addr_pattern, row[1], re.MULTILINE)
                self.addresses.append(f"{self._normalize_address(addr_match.group(1))} {self._normalize_address(addr_match.group(2))}")
                # Increment address counter
                self.count += 1
    
    def _import_distances(self):
        """
        Private method to import distance data from the CSV file.
        """
        # Initialize 2D list for distances with zeros
        self.distances = [[0 for _ in range(self.count)] for __ in range(self.count)]

        with open(self.file, 'r') as file:
            csv_reader = csv.reader(file)
            y = 0
            for row in csv_reader:
                row_dist = row[2:] # Slice row to get distance data
                for x in range(self.count):
                    # If distance value exists, add it to the distances 2D list
                    if len(row_dist[x]) > 0:
                        self.distances[y][x] = float(row_dist[x])
                        self.distances[x][y] = float(row_dist[x]) # Mirror the distance value
                y += 1
    
    def distance(self, addr1, addr2):
        """
        Public method to get the distances between two addresses

        Returns:
            The distance between two addresses
        """
        # Handle HUB address
        if addr1 == "HUB":
            addr1 = "4001 South 700 East"
        if addr2 == "HUB":
            addr2 = "4001 South 700 East"
        # Get distance between the two addresses
        addr1 = self._normalize_address(addr1)
        addr2 = self._normalize_address(addr2)
        addr1_index = self.addresses.index(addr1)
        addr2_index = self.addresses.index(addr2)
        return self.distances[addr1_index][addr2_index]
    
    def _normalize_address(self, addr):
        """
        Normalize the given address by converting it to lowercase and abbreviating cardinal directions.

        Args:
            addr : The address to normalize.

        Returns:
            The normalized address.
        """
        return addr.lower().replace('south','s').replace('west','w').replace('north','n').replace('east','e')

# Test the AddressImporter class
if __name__ == "__main__":
    importer = AddressImporter('distances.csv')
    print(importer.addr_names)
    print(importer.addresses)
    print(importer.distances)
