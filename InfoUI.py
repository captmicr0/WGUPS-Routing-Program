from datetime import datetime, timedelta

class InfoUI:
    """
    A user interface class for displaying package tracking and delivery status information.
    """
    def __init__(self, pkgHashTable, trucks):
        """
        Initialize the InfoUI with package hash table and trucks.

        Args:
            pkgHashTable: Hash table containing package information.
            trucks: List of truck objects used for deliveries.
        """
        self.pkgHashTable = pkgHashTable
        self.trucks = trucks
    
    def mainMenuLoop(self):
        """
        Display the main menu and handle user input in a loop.
        """
        self._clear()
        print("""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------

1. Generate Report
2. View Package Status
3. View Truck Status
4. View Total Mileage
5. Exit
""")
        choice = int(input("Enter your choice (1-5): "))

        # Call method based on user choice
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
        
        # Recursive call to continue the menu loop
        self.mainMenuLoop()
    
    def generateReport(self):
        """
        Generate and display a report of package statuses.
        """
        self._clear()
        print("""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Report Generator --------------------------------------------
--------------------------------------------------------------------
""")
        atTime = self._inputTime()
        if atTime:
            self._generateTimedReport(atTime)
        else:
            self._generateFullReport()

    def _generateTimedReport(self, atTime):
        """
        Generate a report of package statuses at a specific time.

        Args:
            atTime: The time at which to generate the report.
        """
        self._clear()
        print(f"""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Timed Report as of {(datetime.min + atTime).strftime("%I:%M %p")} ---------------------------------
--------------------------------------------------------------------
""")
        totalMiles = 0
        for truck in self.trucks:
            totalMiles += [x[0] for x in truck.mileage_log if x[1] <= atTime][-1]
        print(f"Total Mileage Traveled by All Trucks at {(datetime.min + atTime).strftime("%I:%M %p")}: {totalMiles:4.1f}")
        print()

        pkgReport = [None] * (max([pkg.id for pkg in self.pkgHashTable]) + 1)
        truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
        for pkg in self.pkgHashTable:
            alreadyLoaded = any(["Loaded on truck" in x[0] for x in pkg.status if x[1] <= atTime])
            alreadyDelivered = any(["Delivered" in x[0] for x in pkg.status if x[1] <= atTime])
            pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    (alreadyLoaded and f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " or "Not Loaded        , ") + \
                    (alreadyDelivered and f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}" or "Not Delivered")
            truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
        
        # Per-Truck reporting
        for truckID in range(1, len(self.trucks) + 1):
            print("--------------------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID} - {sum([x[0] for x in self.trucks[truckID-1].mileage_log if x[1] <= atTime]):4.1f} miles - As of {(datetime.min + atTime).strftime("%I:%M %p")} ------------")
            print("--------------------------------------------------------------------")

            for pkgID in truckPkgIDs[truckID]:
                print(pkgReport[pkgID])
        
        # Global reporting
        #for line in pkgReport:
        #    if line:
        #        print(line)

        print("--------------------------------------------------------------------")
        self._waitToContinue()

    def _generateFullReport(self):
        """
        Generate a full report of package statuses for the entire day.
        """
        self._clear()
        print(f"""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Full Report -------------------------------------------------
--------------------------------------------------------------------
""")
        totalMiles = sum([truck.mileage for truck in self.trucks])
        print(f"Total Mileage Traveled by All Trucks: {totalMiles:4.1f} miles")
        print()

        pkgReport = [None] * (max([pkg.id for pkg in self.pkgHashTable]) + 1)
        truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
        for pkg in self.pkgHashTable:
            pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " + \
                    f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}"
            truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
        
        # Per-Truck reporting
        for truckID in range(1, len(self.trucks) + 1):
            print("--------------------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID} -- {self.trucks[truckID-1].mileage:4.1f} miles ----------------------------")
            print("--------------------------------------------------------------------")
            
            for pkgID in truckPkgIDs[truckID]:
                print(pkgReport[pkgID])
        
        # Global reporting
        #for line in pkgReport:
        #    if line:
        #        print(line)
        
        print("--------------------------------------------------------------------")
        self._waitToContinue()

    def packageStatus(self):
        """
        Display the status of a specific package.
        """
        self._clear()
        print("""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Package Status ----------------------------------------------
--------------------------------------------------------------------
""")
        pkgCount = len([pkg for pkg in self.pkgHashTable])
        pkgID = int(input(f"Enter Package ID (1-{pkgCount}): "))

        atTime = self._inputTime()
        print()

        if atTime:
            print(self.pkgHashTable.lookup(pkgID).__str__(atTime))
        else:
            print(self.pkgHashTable.lookup(pkgID))
        
        self._waitToContinue()

    def truckStatus(self):
        """
        Display the status of a specific truck.
        """
        self._clear()
        print("""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Truck Status ------------------------------------------------
--------------------------------------------------------------------
""")
        truckID = int(input(f"Enter Truck ID (1-{len(self.trucks)}): ")) - 1

        atTime = self._inputTime()
        print()
        

        if atTime:
            print(self.trucks[truckID].__str__(atTime))
            print()
            pkgReport = [None] * (max([pkg.id for pkg in self.pkgHashTable]) + 1)
            truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
            for pkg in self.pkgHashTable:
                alreadyLoaded = any(["Loaded on truck" in x[0] for x in pkg.status if x[1] <= atTime])
                alreadyDelivered = any(["Delivered" in x[0] for x in pkg.status if x[1] <= atTime])
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    (alreadyLoaded and f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " or "Not Loaded        , ") + \
                    (alreadyDelivered and f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}" or "Not Delivered")
                truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
            
            print("--------------------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID} - {sum([x[0] for x in self.trucks[truckID-1].mileage_log if x[1] <= atTime]):4.1f} miles - As of {(datetime.min + atTime).strftime("%I:%M %p")} ------------")
            print("--------------------------------------------------------------------")
            for pkgID in truckPkgIDs[truckID+1]:
                print(pkgReport[pkgID])
            print("--------------------------------------------------------------------")
        else:
            print(self.trucks[truckID])
            print()
            pkgReport = [None] * (max([pkg.id for pkg in self.pkgHashTable]) + 1)
            truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
            for pkg in self.pkgHashTable:
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    f"Loaded at {(datetime.min + [x[1] for x in pkg.status if "Loaded on truck" in x[0]][0]).strftime("%I:%M %p")}, " + \
                    f"Delivered at {(datetime.min + [x[1] for x in pkg.status if "Delivered" in x[0]][0]).strftime("%I:%M %p")}"
                truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
            
            print("--------------------------------------------------------------------")
            print(f"--- Packages on Truck #{truckID+1} -- {self.trucks[truckID].mileage:4.1f} miles ----------------------------")
            print("--------------------------------------------------------------------")
            for pkgID in truckPkgIDs[truckID+1]:
                print(pkgReport[pkgID])
            print("--------------------------------------------------------------------")
        
        self._waitToContinue()
        
    def totalMileage(self):
        """
        Display the total mileage traveled by all trucks.
        """
        self._clear()
        print("""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ Truck Mileage -----------------------------------------------
--------------------------------------------------------------------
""")
        atTime = self._inputTime()
        print()

        if atTime:
            totalMiles = 0
            for truck in self.trucks:
                totalMiles += [x[0] for x in truck.mileage_log if x[1] <= atTime][-1]
            print(f"Total Mileage Traveled by All Trucks at {(datetime.min + atTime).strftime("%I:%M %p")}: {totalMiles:4.1f} miles")
        else:
            totalMiles = sum([truck.mileage for truck in self.trucks])
            print(f"Total Mileage Traveled by All Trucks: {totalMiles:.1f} miles")
        self._waitToContinue()
    
    def _inputTime(self):
        """
        Prompt the user to input a time and convert it to a timedelta object.

        Returns:
            The input time converted to a timedelta object, or None if no input is provided.
        """
        timeStr = input("Enter time (HH:MM AM/PM), or press ENTER for all data: ")
        if len(timeStr) == 0:
            return None
        time = datetime.strptime(timeStr, "%I:%M %p")
        return timedelta(hours=time.hour, minutes=time.minute)
    
    def _waitToContinue(self):
        """
        Pause the program execution and wait for user input to continue.

        This function displays a prompt and waits for the user to press ENTER
        before returning to the main menu.
        """
        input("\nPress ENTER to return to the Main Menu...")
    
    def _clear(self):
        """
        Clear the console screen.

        This method uses ANSI escape codes to clear the console screen:
        - \033[H moves the cursor to the top-left corner of the screen
        - \033[J clears the screen from the cursor position to the end
        - \033[3J clears the entire screen and scrollback buffer
        
        Note: This method may not work on all operating systems or terminals.
        """
        print("\033[H\033[3J", end="")
        print("\033[H\033[J", end="")
