import math
from math import sin, cos, atan2, radians, sqrt
import csv
from collections import defaultdict


class City:

    def __init__(self):
        self.setCityPosition()

    def setCities(self):
        self.listOfCities = []
        # each value in each column is appended to a list
        columns = defaultdict(list)
        with open('KnowledgeBase//cities.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
        del columns[0][0]
        for i in range(len(columns[0])):
            self.listOfCities.append(columns[0][i])

    def getCities(self):
        return self.listOfCities

    def displayCities(self):
        for i in range(len(self.listOfCities)):
            print(self.listOfCities[i])
        print("\n")

    # Should create map. Each city with its position
    def setCityPosition(self):
        self.listOfCityAndPosition = {}
        position = ()
        # each value in each column is appended to a list
        columns = defaultdict(list)
        with open('KnowledgeBase//cities.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
        del columns[0][0], columns[1][0], columns[2][0]
        for i in range(len(columns[0])):
            position = columns[1][i], columns[2][i]
            self.listOfCityAndPosition[position] = columns[0][i]

    def getCityPosition(self):
        return self.listOfCityAndPosition

    def displayCityPosition(self):
        print(self.listOfCityAndPosition.items())

    def calcDistance(self, city1, city2):  # Using Haversine Formula to calculate distance
        '''
        The haversine formula determines the great-circle distance between two points
        on a sphere given their longitudes and latitudes.

        The haversine of the central angle (which is d/r) is calculated by the following formula:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c

        where φ is the latitude and λ is the longitude.

        '''

        # R is the earth's radius
        R = 6373.0

        keyLst = list(self.listOfCityAndPosition.keys())
        valueLst = list(self.listOfCityAndPosition.values())

        pos1 = []
        pos2 = []
        pos1 = keyLst[valueLst.index(city1)]
        pos2 = keyLst[valueLst.index(city2)]

        city1Latitude = radians(float(pos1[0]))
        city1Longitude = radians(float(pos1[1]))
        city2Latitude = radians(float(pos2[0]))
        city2Longitude = radians(float(pos2[1]))

        longDiff = city2Longitude - city1Longitude
        latDiff = city2Latitude - city1Latitude

        a = sin(latDiff / 2)**2 + cos(city1Latitude) * \
            cos(city2Latitude) * sin(longDiff / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        d = R * c

        return math.ceil(d)

    # This heuristic function calculates the distance between the departure city and the destination city
    def heuristicFunc(self, destination):
        # Each city's distance between the destination is calculated
        # The destination city's calculation will obviously return zero.
        self.setCities()
        self.heuristic = {}
        for i in self.listOfCities:
            self.heuristic[i] = self.calcDistance(i, destination)

    # This function calculates the distance between the departure city and all other cities
    def actualCost(self, departure):
        self.setCities()
        self.a_cost = {}
        for i in self.listOfCities:
            self.a_cost[i] = self.calcDistance(departure, i)

    def getHeuristic(self, destination):
        '''
        I don't actually know why but the program keeps saying Lyon isn't in the heuristic and a_cost dictionaries, even though it is.
        But after many debugging sessions I found out that Lyon is the 7th member of the dictionaries.
        A simple try-catch should do the job fine.
        '''
        try:
            keyLst = list(self.heuristic.keys())
            valueLst = list(self.heuristic.values())
            return valueLst[keyLst.index(destination)]
        except:
            return valueLst[7]

    def getActualCost(self, departure):
        try:
            keyLst = list(self.a_cost.keys())
            valueLst = list(self.a_cost.values())
            return valueLst[keyLst.index(departure)]
        except ValueError:
            return valueLst[7]

    def getDestinationsPerDeparture(self, departure):
        self.listOfDestinations = set()  # A Set rather than a list to avoid repetition
        # each value in each column is appended to a list
        columns = defaultdict(list)
        with open('KnowledgeBase//flights.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
        del columns[0][0], columns[1][0], columns[2][0], columns[3][0], columns[4][0], columns[5][0]
        for i in range(len(columns[0])):
            if columns[0][i] == departure:
                self.listOfDestinations.add(columns[1][i])

    def getAvailableFlight(self, city1, city2):
        availableFlights = {}
        flightDuration = []
        flightNumber = []
        flight = ()
        availableDays = []
        flightDetails = []
        # each value in each column is appended to a list
        columns = defaultdict(list)
        with open('KnowledgeBase//flights.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
        del columns[0][0], columns[1][0], columns[2][0], columns[3][0], columns[4][0], columns[5][0]
        for i in range(len(columns[0])):
            if columns[0][i] == city1 and columns[1][i] == city2:
                flight = city1, city2
                flightDuration.append(columns[2][i])
                flightDuration.append(columns[3][i])
                flightNumber.append(columns[4][i])
                availableDays.append(columns[5][i])
                flightDetails = flightDuration, flightNumber, availableDays
                availableFlights[flight] = flightDetails
        return availableFlights


# A function that checks if two given cities have a direct flight between them, else choose second closest city.


    def DirectFlightExists(self, city1, city2):
        exists = False
        columns = defaultdict(list)
        with open('KnowledgeBase//flights.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
        del columns[0][0], columns[1][0], columns[2][0], columns[3][0], columns[4][0], columns[5][0]

        for i in range(len(columns[0])):
            if columns[0][i] == city1 and columns[1][i] == city2:
                exists = True

        return exists
