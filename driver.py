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

# Initialize airplanes with arbitrary origin and destination coordinates
a = Airplane('A', Coordinate(2, 2, 0), Coordinate(6, 2, 0))
b = Airplane('B', Coordinate(6, 2, 0), Coordinate(2, 2, 0))
c = Airplane('C', Coordinate(2, 5, 0), Coordinate(6, 5, 0))

# Put airplanes into a list
airplanes = list((a, b, c))
n = len(airplanes)
for i in range(0,n):
    print(airplanes[i])

# Initialize the controller with the airplane list
c = Controller(airplanes)

# 2D Graph generator for aircraft flight paths
def graph():
    # Y axis -- needs twice the range of the x axis so that the | can be printed on every other line
    for y in range(19, -1, -1):
        # X axis
        for x in range(0,10):
            # Plot the airplanes on the graph
            for i in range(0,n):
                if airplanes[i].position is not None and (x == airplanes[i].position.x) and (y/2 == airplanes[i].position.y):
                    if (airplanes[i].position.x == airplanes[i].destination.x) and (airplanes[i].position.y == airplanes[i].destination.y):
                        # Landed symbol
                        s = " L "
                    else:
                        # Airplane traveling symbol
                        s = chr(ord(airplanes[i].identifier))
                        if (airplanes[i].position.z < 10):
                            s = s + "0" + str(airplanes[i].position.z)
                        else:
                            s = s + str(airplanes[i].position.z)
                    break
                else:
                    # Normal coordinate symbol
                    s = " . "
            # Plot the connectors
            if (y%2 == 0):
                if (x != 9):
                    print(s, end = "—")
                else:
                    print(s, end = "")
            elif (y != 0) and (y != 19):
                print(" | ", end = " ")
        print("")

# Run loop
print("====Run Loop====")
for i in range(0,11):
    # Graph and print current positions
    graph()
    print("t-" + str(i))
    for j in range(0,n):
        print("ID" + str(j) + ": " + str(airplanes[j]))

    # Run the controller on the list of airplanes
    airplanes = c.run(airplanes)
    n = len(airplanes)

    # Have the airplanes travel the next timestep
    for j in range(0,n):
        airplanes[j].run()

    # If all planes have landed and stopped broadcasting their location, stop
    if (n == 0):
        break

    sleep(1)