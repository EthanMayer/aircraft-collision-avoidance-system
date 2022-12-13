#   driver.py
#
#   Author: Ethan Mayer
#   Fall 2022

# Includes
from airplane import *
from controller import *
from time import sleep

# Initialize airplane with arbitrary origin and destination coordinates
a = Airplane(Coordinate(2, 2, 0), Coordinate(6, 2, 0))
b = Airplane(Coordinate(6, 2, 0), Coordinate(2, 2, 0))
airplanes = list((a, b))
n = len(airplanes)
for i in range(0,n):
    print(airplanes[i])

# Initialize the controller with the airplane
c = Controller(airplanes)

# 2D Graph generator for aircraft flight paths
def graph():
    for y in range(19, -1, -1):
        for x in range(0,10):
            for i in range(0,n):
                if (x == airplanes[i].position.x) and (y/2 == airplanes[i].position.y):
                    if (airplanes[i].position == airplanes[i].destination):
                        s = "L"
                    else:
                        s = "A"
                    break
                else:
                    s = "o"
            if (y%2 == 0):
                if (x != 9):
                    print(" " + s + " ", end = "—")
                else:
                    print(" " + s, end = "")
            elif (y != 0) and (y != 19):
                print(" | ", end = " ")
        print("")

# Run loop
print("====Run Loop====")
for i in range(0,10):
    graph()
    airplanes = c.run(airplanes)
    print("t-" + str(i))
    for j in range(0,n):
        airplanes[j].run()
        print("ID" + str(j) + ": " + str(airplanes[j]))
    sleep(1)