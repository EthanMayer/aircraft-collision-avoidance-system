#   controller.py
#
#   Author: Ethan Mayer
#   Fall 2022

# Includes
from airplane import *

# Class for the centralized aircraft controller
class Controller:
    # Class variables
    airplane: Airplane
    x_distance: int
    y_distance: int
    z_distance: int
    x_set = False
    y_set = False

    # Class methods
    # Function to calculate the distance the airplane needs to travel
    def calculate_distance(self, airplane: Airplane):
        origin = airplane.origin
        destination = airplane.destination
        self.x_distance = destination.x - origin.x
        self.y_distance = destination.y - origin.y
        # self.z_distance TODO: Altitude calculations
    
    # Function to calculate the heading the plane needs to use
    def calculate_heading(self, airplane: Airplane):
        if not self.y_set:
            if (self.x_distance > 0):
                airplane.heading = Heading.EAST
            elif (self.x_distance < 0):
                airplane.heading = Heading.WEST
            self.x_set = True
        if not self.x_set:
            if (self.y_distance > 0):
                airplane.heading = Heading.NORTH
            elif (self.y_distance < 0):
                airplane.heading = Heading.SOUTH
            self.y_set = True

    
        

