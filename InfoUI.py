import re
from datetime import datetime, timedelta

class InfoUI:
    def __init__(self, pkgHashTable, trucks):
        self.pkgHashTable = pkgHashTable
        self.trucks = trucks
    
    def mainMenuLoop(self):
        self._clear()
        print(\
"""WGUPS Package Tracking and Delivery Status
------------------------------------------

1. View Package Status
2. View Truck Status
3. View Total Mileage
4. Exit
""")
        choice = int(input("Enter your choice (1-4): "))

        if choice == 1:
            self.packageStatus()
        elif choice == 2:
            self.truckStatus()
        elif choice == 3:
            self.totalMileage()
        elif choice == 4:
            print("Thank you for using WGUPS Package Tracking. Goodbye!")
            return
        
        self.mainMenuLoop()

    def packageStatus(self):
        self._clear()
        pkgCount = len([pkg for bucket in self.pkgHashTable.table for _, pkg in bucket])
        pkgID = int(input(f"Enter Package ID (1-{pkgCount}): "))
        print(self.pkgHashTable.lookup(pkgID))
        self._waitToContinue()

    def truckStatus(self):
        self._clear()
        truckID = int(input(f"Enter Truck ID (1-{len(self.trucks)}): ")) - 1
        print(self.trucks[truckID])
        self._waitToContinue()
        
    def totalMileage(self):
        self._clear()
        totalMiles = sum([truck.mileage for truck in self.trucks])
        print(f"Total Mileage Traveled by All Trucks: {totalMiles}")
        self._waitToContinue()
    
    def _inputTime(self):
        timeStr = input("Enter time (HH:MM AM/PM): ")
        time = re.search(r"([0-9]{1,2})\:([0-9]{2})", timeStr)
        return timedelta(hours=('PM' in timeStr and 12 or 0) + int(time.group(1)),
                         minutes=int(time.group(2)))
    
    def _waitToContinue(self):
        input("\nPress ENTER to return to the Main Menu...")
    
    def _clear(self):
        """
        Clear the console screen.

        This method uses ANSI escape codes to clear the console screen:
        - \033[H moves the cursor to the top-left corner of the screen
        - \033[J clears the screen from the cursor position to the end
        
        Note: This method may not work on all operating systems or terminals.
        """
        print("\033[H\033[J", end="")
