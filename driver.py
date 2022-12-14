#   driver.py
#
#   Author: Ethan Mayer
#   Fall 2022
#
#   This file is the driver for the aircraft controller. All airplanes are instantiated and all controller tests are found here.

# Includes
from airplane import *
from controller import *
from time import sleep

# 2D Graph generator for aircraft flight paths
def graph():
    # Y axis -- needs twice the range of the x axis so that the | can be printed on every other line
    for y in range(19, -1, -1):

        # X axis
        for x in range(0,10):

            # Plot the airplanes on the graph
            for i in range(0,n):

                # Normal coordinate symbol
                s = " · "

                if airplanes[i].position is None:

                    # Check if airplane has landed
                    if (x == airplanes[i].destination.x) and (y/2 == airplanes[i].destination.y):
                        # Landed symbol
                        s = " L!"
                        break

                # Check if airplane is still traveling
                elif (x == airplanes[i].position.x) and (y/2 == airplanes[i].position.y):

                    # Airplane traveling symbol is its identifier + altitude
                    s = chr(ord(airplanes[i].identifier))
                    if (airplanes[i].position.z < 10):
                        s = s + "0" + str(airplanes[i].position.z)
                    else:
                        s = s + str(airplanes[i].position.z)
                    break

            # Plot the connectors (graph edges)
            if (y%2 == 0):
                if (x != 9):
                    print(s, end = "—")
                else:
                    print(s, end = "")
            elif (y != 0) and (y != 19):
                print(" | ", end = " ")
        print("")

############### Start of script

# Prompt user for demo selection
print("Aircraft Collision Avoidance System Demo:")
print("Which demo would you like to run? (Please enter a digit)")
print("1 Two Aircraft Routing")
print("2 Four Aircraft Routing")
print("3 Eight Aircraft Routing")

# Grab user input
demo = input()

# Select demo and initialize airplanes with randomly generated origin and destination coordinates
if (demo == "1"):
    a = Airplane('A', Coordinate(2, 2, 0), Coordinate(6, 2, 0))
    b = Airplane('B', Coordinate(6, 2, 0), Coordinate(2, 2, 0))

    # Put airplanes into a list
    airplanes = list((a, b))
    n = len(airplanes)
elif (demo == "2"):
    a = Airplane('A', Coordinate(2, 2, 0), Coordinate(6, 2, 0))
    b = Airplane('B', Coordinate(6, 2, 0), Coordinate(2, 2, 0))
    c = Airplane('C', Coordinate(2, 5, 0), Coordinate(6, 5, 0))
    d = Airplane('D', Coordinate(5, 5, 0), Coordinate(1, 1, 0))

    # Put airplanes into a list
    airplanes = list((a, b, c, d))
    n = len(airplanes)
elif (demo == "3"):
    a = Airplane('A', Coordinate(2, 2, 0), Coordinate(6, 2, 0))
    b = Airplane('B', Coordinate(6, 2, 0), Coordinate(2, 2, 0))
    c = Airplane('C', Coordinate(2, 5, 0), Coordinate(6, 5, 0))
    d = Airplane('D', Coordinate(5, 5, 0), Coordinate(1, 1, 0))
    e = Airplane('E', Coordinate(8, 2, 0), Coordinate(9, 5, 0))
    f = Airplane('F', Coordinate(0, 0, 0), Coordinate(1, 9, 0))
    g = Airplane('G', Coordinate(1, 9, 0), Coordinate(2, 8, 0))
    h = Airplane('H', Coordinate(9, 9, 0), Coordinate(9, 0, 0))
    i = Airplane('I', Coordinate(6, 0, 0), Coordinate(9, 1, 0))

    # Put airplanes into a list
    airplanes = list((a, b, c, d, e, f, g, h, i))
    n = len(airplanes)

# Print starting airplanes
for i in range(0,n):
    print(airplanes[i])

# Initialize the controller with the airplane list
c = Controller(airplanes)

# Run loop
print("====Run Loop====")
i = 0
while(1):
    # Graph and print current positions
    graph()
    print("t-" + str(i))
    i = i + 1
    for j in range(0,n):
        print("ID " + airplanes[j].identifier + ": " + str(airplanes[j]))

    # Run the controller on the list of airplanes
    airplanes = c.calculate_next_maneuver(airplanes)
    n = len(airplanes)

    # Have the airplanes travel the next timestep (1 minute)
    for j in range(0,n):
        airplanes[j].fly_one_timestep()

    # If all planes have landed and stopped broadcasting their location, stop
    if (n == 0):
        break

    # Sleep simulation 1 second to emulate 1 minute timestep (flight events occur, airplane moves along current heading, communication delay, etc.)
    sleep(1)