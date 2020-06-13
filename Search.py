from City import City
from Flight import Flight


visitedCities = []
parentOfNode = {}
previousNode = {}
finalResult = []


class Search:

    def __init__(self):
        self.daysOfWeek = []
        self.inititalDeparture = ''
        self.citiesToVisit = {}
        self.goToCity = ''
        self.counter = 0
        self.tempValue = 2**63
        self.minValue = 2**63
        self.tempDict = {}
        self.flag = False
        self.keyLst = []
        self.valueLst = []
        self.keyLst2 = []
        self.valueLst2 = []
        self.flightDetails = []
        self.firstFlight = False
        self.cty = City()
        self.listOfFlightDays = []
        self.previousDay = ''
        self.currentDay = ''
        self.previousTime = ''
        self.currentTime = ''

    def setDeparture(self, departure):
        self.departure = departure

    def getDeparture(self):
        return self.departure

    def setDestination(self, destination):
        self.destination = destination

    def getDestination(self):
        return self.destination

    def checkIfNextDay(self, time1, time2):  # checks if the arrival time is next day
        status = False
        hr_mins = 60
        if len(time1) == 4:
            time1_hrs = time1[0]
            time1_mins = time1[2] + time1[3]
        elif len(time1) == 5:
            time1_hrs = time1[0] + time1[1]
            time1_mins = time1[3] + time1[4]

        if len(time2) == 4:
            time2_hrs = time2[0]
            time2_mins = time2[2] + time2[3]
        elif len(time2) == 5:
            time2_hrs = time2[0] + time2[1]
            time2_mins = time2[3] + time2[4]

        newTime1 = int(time1_hrs) * hr_mins + int(time1_mins)
        newTime2 = int(time2_hrs) * hr_mins + int(time2_mins)
        timeDifference = newTime2 - newTime1

        if timeDifference < 0:
            status = True

        return status

    def getDifference(self, time):  # gets the time difference between two given times
        hr_mins = 60
        if len(time) == 4:
            time_hrs = time[0]
            time_mins = time[2] + time[3]
        elif len(time) == 5:
            time_hrs = time[0] + time[1]
            time_mins = time[3] + time[4]

        if len(self.currentTime) == 4:
            ct_hrs = self.currentTime[0]
            ct_mins = self.currentTime[2] + self.currentTime[3]
        elif len(self.currentTime) == 5:
            ct_hrs = self.currentTime[0] + self.currentTime[1]
            ct_mins = self.currentTime[3] + self.currentTime[4]

        newTime = int(time_hrs) * hr_mins + int(time_mins)
        newCT = int(ct_hrs) * hr_mins + int(ct_mins)
        timeDifference = newTime - newCT

        return timeDifference

    def getNearestTime(self):  # gets the nearest time to the current time
        listOfTimes = []
        originalTimes = []
        oldTime_newTime = {}
        for iterator in range(0, len(self.flightDetails[0])):
            originalTimes.append(self.flightDetails[0][iterator])
            if iterator % 2 == 0:
                listOfTimes.append(self.flightDetails[0][iterator])
                oldTime_newTime[self.flightDetails[0][iterator]] = 0

        for i in range(0, len(listOfTimes)):
            oldTime_newTime[listOfTimes[i]
                            ] = self.getDifference(listOfTimes[i])
            listOfTimes[i] = self.getDifference(listOfTimes[i])

        keyLst = list(oldTime_newTime.keys())
        valueLst = list(oldTime_newTime.values())
        if all(i >= 0 for i in listOfTimes) == True:
            index = min(listOfTimes)
        else:
            index = max(listOfTimes)

        index = keyLst[valueLst.index(index)]

        valueIndex = originalTimes.index(index)

        return valueIndex

    def getNextDay(self, day):  # takes a day and return the next day (e.g. given: sat, returns: sun)
        days = self.daysOfWeek
        index = days.index(day)
        try:
            return days[index+1]
        except:
            return days[0]

    # sets a newer flight day range. (old: sun,mon,tue. new: sat,sun,mon,tue,wed)
    def newFlightDays(self):
        startDay = self.listOfFlightDays[0]
        endDay = self.listOfFlightDays[-1]

        startIndex = self.daysOfWeek.index(startDay)
        endIndex = self.daysOfWeek.index(endDay)

        newStartIndex = startIndex - 1
        newEndIndex = endIndex + 1

        self.listOfFlightDays = self.daysOfWeek[newStartIndex:newEndIndex+1]
        print("------No path found within the given day range, therefore that range has been widened-------")

    def outputSteps(self):  # Outputs the final steps to the console
        print("\n")
        availableFlights = {}
        flight = ()
        flightNumber = ''
        numberOfSteps = len(visitedCities) - 1
        self.flag = False
        self.previousTime = '00:00'
        self.currentTime = '00:00'

        for i in range(1, numberOfSteps+1):
            if i == 1:
                self.firstFlight = True
            else:
                self.firstFlight = False
            iterationFlag = False
            flight = (visitedCities[i-1], visitedCities[i])
            availableFlights = self.cty.getAvailableFlight(
                visitedCities[i-1], visitedCities[i])
            self.flightDetails = availableFlights[flight]
            # number of iterations for each possible flight
            iteration = len(self.flightDetails[2])
            for j in range(iteration):
                self.flightDetails[2][j] = self.flightDetails[2][j].strip(
                    '[]').split(',')
                self.flightDetails[2][j] = [
                    lst.strip(' ') for lst in self.flightDetails[2][j]]

            for j in range(iteration):
                if iterationFlag == True:
                    break
                elif self.previousDay in self.flightDetails[2][j]:
                    self.currentDay = self.previousDay
                    index = j
                    break
                for k in self.flightDetails[2][j]:
                    if k in self.listOfFlightDays:
                        if not self.firstFlight:
                            if self.daysOfWeek.index(k) > self.daysOfWeek.index(self.previousDay):
                                pass
                            else:
                                break
                        self.currentDay = k
                        index = j
                        iterationFlag = True
                        break
            if self.currentDay == '':
                # here means there's no day in the flight's range that suits this person's desired day range
                self.newFlightDays()  # widen the range
                for j in range(iteration):  # check for a flight again
                    if iterationFlag == True:
                        break
                    elif self.previousDay in self.flightDetails[2][j]:
                        self.currentDay = self.previousDay
                        index = j
                        break
                    for k in self.flightDetails[2][j]:
                        if k in self.listOfFlightDays:
                            self.currentDay = k
                            index = j
                            iterationFlag = True
                            break

            if self.firstFlight == False:
                index = self.getNearestTime()

            # get departure time
            DepartureTime = str(self.flightDetails[0][index])
            #del flightDetails[0][index]

            # get arrival time
            ArrivalTime = str(self.flightDetails[0][index+1])
            #del flightDetails[0][index]

            self.previousTime = DepartureTime
            self.currentTime = ArrivalTime
            status = self.checkIfNextDay(self.previousTime, self.currentTime)
            if status == True:
                self.currentDay = self.getNextDay(self.currentDay)

            flightNumber = self.flightDetails[1][int(index/2)]
            self.previousDay = self.currentDay
            self.currentDay = ''
            #del flightDetails[1][0]
            print("Step " + str(i) + ": " + "Use Flight " + flightNumber + " From " +
                  str(visitedCities[i-1]) + " To " + str(visitedCities[i]) + ". Departure Time: " + DepartureTime + " and Arrival Time: " + ArrivalTime)

    def findMinimum(self):  # finds minimum value in citiesToVisit dictionary to get the go to city
        self.keyLst = list(self.citiesToVisit.keys())
        self.valueLst = list(self.citiesToVisit.values())
        self.minValue = 2**63

        for i in self.keyLst:
            if i == self.departure:
                self.citiesToVisit[i] = self.tempValue

            elif self.valueLst[self.keyLst.index(i)] < self.minValue:
                self.minValue = self.valueLst[self.keyLst.index(i)]

        return self.minValue

    # this is for when the previous city caused problems with the final output so we find a new minimum
    def findNewMinimum(self, city):
        # the problem was there was no direct flight between a departure city and a destinations city
        self.keyLst = list(self.citiesToVisit.keys())
        self.valueLst = list(self.citiesToVisit.values())
        del self.citiesToVisit[city]
        self.minValue = 2**63

        for i in self.keyLst:
            if i == self.departure:
                continue

            elif self.valueLst[self.keyLst.index(i)] < self.minValue:
                self.minValue = self.valueLst[self.keyLst.index(i)]
        return self.minValue

    def getFinalResult(self):
        result = []
        result.append(self.destination)
        for i in range(len(visitedCities) - 1, -1, -1):
            if visitedCities[i] == self.inititalDeparture:
                pass
            else:
                result.append(previousNode[visitedCities[i]])

        return result[::-1]

    # When there's no direct flight, we choose another nearest city
    def pickNewFlight(self, status):
        newGoToCity = self.goToCity
        del previousNode[self.departure]
        city = visitedCities.pop()
        self.departure = visitedCities[-1]
        newMinimum = self.findNewMinimum(city)
        previousNode[newGoToCity] = self.departure
        if self.flag == False:
            self.goToCity = self.keyLst[self.valueLst.index(newMinimum)]
        else:
            self.goToCity = self.keyLst2[self.valueLst2.index(newMinimum)]

    # to get the sum of the heuristic value and actual edge cost of a node
    def getTotalDistance(self, node):
        actualDistance = 0
        heuristicDistance = 0
        totalDistance = 0

        self.cty.heuristicFunc(self.getDestination())
        self.cty.actualCost(self.getDeparture())

        actualDistance = self.cty.getActualCost(node)
        heuristicDistance = self.cty.getHeuristic(node)
        totalDistance = actualDistance + heuristicDistance

        return totalDistance

    # To find the shortest path between initial departure and destination
    def searchAlgorithm(self, departure, destination):

        self.departure = departure
        visitedCities.append(departure)
        self.cty.getDestinationsPerDeparture(departure)
        sameValues = list(set(visitedCities) &
                          set(self.cty.listOfDestinations))

        exists = False
        if(sameValues != []):
            for i in sameValues:
                self.cty.actualCost(departure)
                self.citiesToVisit[i] = self.cty.getActualCost(
                    i)**2 + self.getTotalDistance(i)

        for i in self.cty.listOfDestinations:
            if i in sameValues:
                continue
            else:
                self.citiesToVisit[i] = self.getTotalDistance(i)

        # parentOfNode[self.departure] = self.cty.listOfDestinations

        minimum_value = self.findMinimum()

        if self.flag == False:
            self.goToCity = self.keyLst[self.valueLst.index(minimum_value)]
        else:
            self.goToCity = self.keyLst2[self.valueLst2.index(minimum_value)]

        previousNode[self.goToCity] = self.departure

        exists = self.cty.DirectFlightExists(self.departure, self.goToCity)

        while(exists != True):
            self.pickNewFlight(exists)
            exists = self.cty.DirectFlightExists(self.departure, self.goToCity)

        if self.goToCity == destination:
            visitedCities.append(destination)
            # Stop here and print solution

            self.outputSteps()
        else:
            # Keep searching for best solution

            self.searchAlgorithm(self.goToCity, destination)
