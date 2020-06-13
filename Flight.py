class Flight:

    def setFlightDetails(self, departureCity, destinationCity, listOfDays, listOfFlightDays):
        self.departureCity = departureCity
        self.destinationCity = destinationCity
        self.listOfDays = listOfDays
        self.listOfFlightDays = listOfFlightDays

    def inputFlightDetails(self):
        self.departureCity = input("Departure City: ").title()
        self.destinationCity = input("Destination City: ").title()
        city1 = self.departureCity
        city2 = self.destinationCity

        if city1 == city2:
            raise Exception(
                "The departure and destination cities are the same!")

        # Here the user enters their desired range of days to fly on
        day1 = input(
            "Enter The Day You Want To Fly On(In \'sat\', \'sun\',.. format): ")
        day2 = input(
            "Enter The Day You Want To Arrive On/Before(In \'sat\', \'sun\',.. format): ")
        # Returns the days in between the two city ranges
        self.generateDaysInBetween(day1, day2)
        self.listOfFlightDays = self.listOfDays[self.index1:self.index2+1]
        # Ex. [Saturday, Monday] ==> Returns [Saturday, Sunday, Monday]

    def getInitialDeparture(self):  # The initial departure city
        return self.departureCity

    def displayFlightDetails(self):
        print("\nDeparture City: " + str(self.departureCity) + "\n" + "Destination City: " + str(self.destinationCity) +
              "\n" + "Days Of The Week You'll Be Flying Through: " + str(self.listOfFlightDays) + "\n")

    def generateDaysInBetween(self, day1, day2):
        self.listOfDays = [
            'sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri']
        if day1 not in self.listOfDays:
            raise Exception("Please write the days in requested format!")
        elif day2 not in self.listOfDays:
            raise Exception("Please write the days in requested format!")
        self.index1 = self.listOfDays.index(day1)
        self.index2 = self.listOfDays.index(day2)

    def getFlightOfDays(self):
        return self.listOfFlightDays

    def getListOfDays(self):
        return self.listOfDays

    def thankYou(self):
        print("\n\nThank You For Choosing AI Research Airways!")
