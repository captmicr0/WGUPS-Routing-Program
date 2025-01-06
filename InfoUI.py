import re
from datetime import datetime, timedelta

### NEED TO IMPLEMENT PER-TRUCK GROUPING IN REPORTS

class InfoUI:
    def __init__(self, pkgHashTable, trucks):
        self.pkgHashTable = pkgHashTable
        self.trucks = trucks
    
    def mainMenuLoop(self):
        self._clear()
        print("""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------

1. Generate Report
2. View Package Status
3. View Truck Status
4. View Total Mileage
5. Exit
""")
        choice = int(input("Enter your choice (1-5): "))

        if choice == 1:
            self.generateReport()
        elif choice == 2:
            self.packageStatus()
        elif choice == 3:
            self.truckStatus()
        elif choice == 4:
            self.totalMileage()
        elif choice == 5:
            print("Thank you for using WGUPS Package Tracking. Goodbye!")
            return
        
        self.mainMenuLoop()
    
    def generateReport(self):
        self._clear()
        print("""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Report Generator ------------------------------
------------------------------------------------------
""")
        atTime = self._inputTime()
        if atTime:
            self._generateTimedReport(atTime)
        else:
            self._generateFullReport()

    def _generateTimedReport(self, atTime):
        self._clear()
        print(f"""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Timed Report as of {(datetime.min + atTime).strftime("%I:%M %p")} -------------------
------------------------------------------------------
""")
        totalMiles = 0
        for truck in self.trucks:
            totalMiles += [x[0] for x in truck.mileage_log if x[1] <= atTime][-1]
        print(f"Total Mileage Traveled by All Trucks at {(datetime.min + atTime).strftime("%I:%M %p")}: {totalMiles:.1f}")
        print()

        pkgReport = [None] * (max([pkg.id for bucket in self.pkgHashTable.table for _, pkg in bucket]) + 1)
        truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
        for bucket in self.pkgHashTable.table:
            for _, pkg in bucket:
                alreadyLoaded = any(["Loaded on truck" in x[0] for x in pkg.status if x[1] <= atTime])
                alreadyDelivered = any(["Delivered" in x[0] for x in pkg.status if x[1] <= atTime])
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                      (alreadyLoaded and f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " or "Not Loaded        , ") + \
                      (alreadyDelivered and f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}" or "Not Delivered")
                truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
        
        # Per-Truck reporting
        for truckID in range(1, len(self.trucks) + 1):
            print("------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID} -- {self.trucks[truckID-1].mileage:4.1f} miles --------------")
            for pkgID in truckPkgIDs[truckID]:
                print(pkgReport[pkgID])
        
        # Global reporting
        #for line in pkgReport:
        #    if line:
        #        print(line)

        print("------------------------------------------------------")
        self._waitToContinue()

    def _generateFullReport(self):
        self._clear()
        print(f"""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Full Report -----------------------------------
------------------------------------------------------
""")
        totalMiles = sum([truck.mileage for truck in self.trucks])
        print(f"Total Mileage Traveled by All Trucks: {totalMiles:.1f} miles")
        print()

        pkgReport = [None] * (max([pkg.id for bucket in self.pkgHashTable.table for _, pkg in bucket]) + 1)
        truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
        for bucket in self.pkgHashTable.table:
            for _, pkg in bucket:
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                      f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " + \
                      f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}"
                truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
        
        # Per-Truck reporting
        for truckID in range(1, len(self.trucks) + 1):
            print("------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID} -- {self.trucks[truckID-1].mileage:4.1f} miles --------------")
            
            for pkgID in truckPkgIDs[truckID]:
                print(pkgReport[pkgID])
        
        # Global reporting
        #for line in pkgReport:
        #    if line:
        #        print(line)
        
        print("------------------------------------------------------")
        self._waitToContinue()

    def packageStatus(self):
        self._clear()
        print("""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Package Status --------------------------------
------------------------------------------------------
""")
        pkgCount = len([pkg for bucket in self.pkgHashTable.table for _, pkg in bucket])
        pkgID = int(input(f"Enter Package ID (1-{pkgCount}): "))

        atTime = self._inputTime()
        print()

        if atTime:
            print(self.pkgHashTable.lookup(pkgID).__str__(atTime))
        else:
            print(self.pkgHashTable.lookup(pkgID))
        
        self._waitToContinue()

    def truckStatus(self):
        self._clear()
        print("""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Truck Status ----------------------------------
------------------------------------------------------
""")
        truckID = int(input(f"Enter Truck ID (1-{len(self.trucks)}): ")) - 1

        atTime = self._inputTime()
        print()

        if atTime:
            print(self.trucks[truckID].__str__(atTime))
        else:
            print(self.trucks[truckID])
        
        self._waitToContinue()
        
    def totalMileage(self):
        print("""
------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status -------
------------------------------------------------------
------ Truck Mileage ---------------------------------
------------------------------------------------------
""")
        self._clear()
        atTime = self._inputTime()
        print()

        if atTime:
            totalMiles = 0
            for truck in self.trucks:
                totalMiles += [x[0] for x in truck.mileage_log if x[1] <= atTime][-1]
            print(f"Total Mileage Traveled by All Trucks at {(datetime.min + atTime).strftime("%I:%M %p")}: {totalMiles:.1f} miles")
        else:
            totalMiles = sum([truck.mileage for truck in self.trucks])
            print(f"Total Mileage Traveled by All Trucks: {totalMiles:.1f} miles")
        self._waitToContinue()
    
    def _inputTime(self):
        timeStr = input("Enter time (HH:MM AM/PM), or press ENTER for all data: ")
        if len(timeStr) == 0:
            return None 
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
