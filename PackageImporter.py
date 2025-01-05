import csv
from datetime import datetime, timedelta

from Package import Package

class PackageImporter:
    """
    A class for importing package data from a CSV file and creating Package objects.
    """
    def __init__(self, file):
        """
        Initialize the PackageImporter with the given CSV file and process its contents.

        Args:
            file: Path to the CSV file containing package data.
        """
        self.file = file
        self.packages = [] # List to store packages
        self._import_packages() # Import package data

    def _import_packages(self):
        """
        Private method to process the CSV file and create Package objects.

        This method reads the CSV file, creates Package objects from each row,
        and appends them to the self.packages list.
        """
        with open(self.file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None) # Skip the headers
            for row in csv_reader:
                pkg = Package(
                    int(row[0]), # PackageID
                    row[1], # Address
                    row[2], # City
                    row[3], # State
                    int(row[4]), # Zip
                    'EOD' in row[5] and None or (datetime.min + timedelta(days=float(row[5]))).strftime('%H:%M'), # DeliveryDeadline
                    float(row[6]), # WeightKILO
                    row[7]) # SpecialNotes
                self.packages.append(pkg)

    def getPackages(self):
        """
        Public method to retrieve the list of imported Package objects.

        Returns:
            A list of Package objects created from the CSV data.
        """
        return self.packages

# Test the PackageImporter class
if __name__ == "__main__":
    importer = PackageImporter('packages.csv')
    for pkg in importer.packages:
        print(pkg)
