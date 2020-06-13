from Flight import Flight
from City import City
from Search import Search


class Interface:

    def Execute(self):

        flight = Flight()
        cty = City()
        searchObj = Search()

        # cty.setCities()
        cty.setCities()  # Get all cities from the knowledge base and store it in a list
        # Get all positions (in Longitude and Latitude Format) for each city
        # cty.displayCities()

        cty.setCityPosition()
        print("\nWelcome to AI Research Airways")
        print("We Can Take You To These Cities Below\n")
        cty.displayCities()  # Prints all cities in console

        flight.inputFlightDetails()  # User enter their desired flight's information
        print("\n------To Continue, Are These Flight Details Below Correct? (Answer With Y or N Only)------")
        flight.displayFlightDetails()  # Displays the flight's details entered by the user
        answer = input("Answer: ")
        while(answer.upper() != 'Y'):
            if answer.upper() == 'N':
                print("------PLease Re=enter Your Flight Details-----\n")
                flight.inputFlightDetails()
                print(
                    "\n------To Continue, Are These Flight Details Below Correct? (Answer With Y or N Only)------")
                flight.displayFlightDetails()
                answer = input("Answer: ")
            else:
                print("Please Answer With Only Y or N!\n")
                print(
                    "\n------To Continue, Are These Flight Details Below Correct? (Answer With Y or N Only)------")
                flight.displayFlightDetails()
                answer = input("Answer: ")

        searchObj.daysOfWeek = flight.getListOfDays()
        searchObj.listOfFlightDays = flight.getFlightOfDays()

        city1 = flight.departureCity
        city2 = flight.destinationCity
        searchObj.setDeparture(city1)
        searchObj.setDestination(city2)
        searchObj.searchAlgorithm(city1, city2)

        flight.thankYou()
