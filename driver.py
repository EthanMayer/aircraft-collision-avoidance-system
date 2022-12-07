#   driver.py
#
#   Author: Ethan Mayer
#   Fall 2022

# Includes
from airplane import *
from controller import *
from time import sleep

# Initialize airplane with arbitrary origin and destination coordinates
origin = Coordinate(2, 2, 0)
destination = Coordinate(4, 2, 0)
a = Airplane(origin, destination)
print(a)

# Initialize the controller with the airplane
c = Controller(a)

print("====Run Loop====")
for i in range(1,4):
    a.heading = c.run(a)
    a.run()
    print(a)
    sleep(1)