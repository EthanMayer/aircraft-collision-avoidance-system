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

print("====Run Loop====")
for i in range(0,10):
    airplanes = c.run(airplanes)
    print("t-" + str(i))
    for j in range(0,n):
        airplanes[j].run()
        print("ID" + str(j) + ": " + str(airplanes[j]))
    sleep(1)