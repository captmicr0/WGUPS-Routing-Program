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
            self.displayStatus("Package")
        elif choice == 3:
            self.displayStatus("Truck")
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
            self._generate_report(atTime)
        else:
            self._generate_report()

    def _generate_package_report(self, atTime=None):
        pkgReport = [None] * (max([pkg.id for pkg in self.pkgHashTable]) + 1)
        truckPkgIDs = [[] for _ in range(len(self.trucks) + 1)]
        
        for pkg in self.pkgHashTable:
            if atTime:
                alreadyLoaded = any(["Loaded on truck" in x[0] for x in pkg.status if x[1] <= atTime])
                alreadyDelivered = any(["Delivered" in x[0] for x in pkg.status if x[1] <= atTime])
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    (alreadyLoaded and f"Loaded at {(datetime.min + [x[1] for x in pkg.status if 'Loaded on truck' in x[0]][0]).strftime('%I:%M %p')}, " or "Not Loaded , ") + \
                    (alreadyDelivered and f"Delivered at {(datetime.min + [x[1] for x in pkg.status if 'Delivered' in x[0]][0]).strftime('%I:%M %p')}," or "Not Delivered, ") + \
                    f"Deadline: {pkg.deadline and (datetime.min + pkg.deadline).strftime('%I:%M %p') or "EOD"}\n" + \
                    f"           Address: {pkg.getAddress()}"
            else:
                pkgReport[pkg.id] = f"Package #{pkg.id:02}: " + \
                    f"Loaded at {(datetime.min + [x[1] for x in pkg.status if 'Loaded on truck' in x[0]][0]).strftime('%I:%M %p')}, " + \
                    f"Delivered at {(datetime.min + [x[1] for x in pkg.status if 'Delivered' in x[0]][0]).strftime('%I:%M %p')}, " + \
                    f"Deadline: {pkg.deadline and (datetime.min + pkg.deadline).strftime('%I:%M %p') or "EOD"}\n" + \
                    f"           Address: {pkg.getAddress()}"
            truckPkgIDs[pkg.isOnTruck()].append(pkg.id)
        
        return pkgReport, truckPkgIDs

    def _print_truck_packages(self, truckID, pkgReport, truckPkgIDs, mileage, atTime=None):
        print("--------------------------------------------------------------------")
        if atTime:
            print(f"--- Packages on Truck #{truckID} - {mileage:06.1f} miles - As of {(datetime.min + atTime).strftime('%I:%M %p')} -----------")
        else:
            print(f"--- Packages on Truck #{truckID} -- {mileage:06.1f} miles ---------------------------")
        print("--------------------------------------------------------------------")
        for pkgID in truckPkgIDs[truckID]:
            print(pkgReport[pkgID])
        print("--------------------------------------------------------------------")
    
    def _generate_report(self, atTime=None):
        self._clear()
        print(f"""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ {'Timed' if atTime else 'Full'} Report {'as of ' + (datetime.min + atTime).strftime("%I:%M %p ") if atTime else ('-' * (15 if atTime else 16))}---------------------------------
--------------------------------------------------------------------
""")

        totalMiles = sum([truck.mileage if not atTime else [x[0] for x in truck.mileage_log if x[1] <= atTime][-1] for truck in self.trucks])
        print(f"Total Mileage Traveled by All Trucks{(' at ' + (datetime.min + atTime).strftime('%I:%M %p')) if atTime else ''}: {totalMiles:06.1f}")
        print()

        pkgReport, truckPkgIDs = self._generate_package_report(atTime)

        for truckID in range(1, len(self.trucks) + 1):
            mileage = self.trucks[truckID-1].mileage if not atTime else [x[0] for x in self.trucks[truckID-1].mileage_log if x[1] <= atTime][-1]
            self._print_truck_packages(truckID, pkgReport, truckPkgIDs, mileage, atTime)

        self._waitToContinue()

    def displayStatus(self, statusType):
        self._clear()
        print(f"""
--------------------------------------------------------------------
--- WGUPS Package Tracking and Delivery Status ---------------------
--------------------------------------------------------------------
------ {statusType.ljust(7)} Status ----------------------------------------------
--------------------------------------------------------------------
""")

        if statusType == "Package":
            pkgCount = len([pkg for pkg in self.pkgHashTable])
            itemID = int(input(f"Enter Package ID (1-{pkgCount}): "))
        elif statusType == "Truck":
            itemID = int(input(f"Enter Truck ID (1-{len(self.trucks)}): ")) - 1

        atTime = self._inputTime()
        print()

        if statusType == "Package":
            print(self.pkgHashTable.lookup(itemID).__str__(atTime) if atTime else self.pkgHashTable.lookup(itemID))
        elif statusType == "Truck":
            if atTime:
                print(self.trucks[itemID].__str__(atTime))
                pkgReport, truckPkgIDs = self._generate_package_report(atTime)
                mileage = [x[0] for x in self.trucks[itemID].mileage_log if x[1] <= atTime][-1]
                self._print_truck_packages(itemID + 1, pkgReport, truckPkgIDs, mileage, atTime)
            else:
                print(self.trucks[itemID])
                pkgReport, truckPkgIDs = self._generate_package_report()
                self._print_truck_packages(itemID + 1, pkgReport, truckPkgIDs, self.trucks[itemID].mileage)

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
            print(f"Total Mileage Traveled by All Trucks at {(datetime.min + atTime).strftime("%I:%M %p")}: {totalMiles:06.1f} miles")
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
