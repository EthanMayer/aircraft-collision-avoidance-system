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
    heading: Heading
    x_set = False
    y_set = False
    x_o: int = 0 # TODO: Temporary other airplane coordinate
    y_o: int = 0 # TODO: Temporary other airplane coordinate

    # Class methods
    # Function to calculate the distance the airplane needs to travel
    def calculate_distance(self, airplane: Airplane):
        origin = airplane.origin
        destination = airplane.destination
        self.x_distance = destination.x - origin.x
        self.y_distance = destination.y - origin.y
        # self.z_distance TODO: Altitude calculations
    
    # Function to calculate the heading the plane needs to use
    def calculate_heading(self):
        # Traverse either x axis or y axis one at a time, prioritizing x axis
        if not self.y_set:
            if (self.x_distance > 0):
                self.heading = Heading.EAST
            elif (self.x_distance < 0):
                self.heading = Heading.WEST
            self.x_set = True
        if not self.x_set:
            if (self.y_distance > 0):
                self.heading = Heading.NORTH
            elif (self.y_distance < 0):
                self.heading = Heading.SOUTH
            self.y_set = True

    # Function to check for possible collisions
    def check_for_collision(self, airplane: Airplane):
        # Check for collision along the x axis and have all planes turn right if true
        if self.x_set and (self.x_o == airplane.position.x - (self.x_distance - 1)):
            if (self.heading == Heading.EAST):
                self.heading = Heading.SOUTH
            elif (self.heading == Heading.WEST):
                self.heading = Heading.NORTH
            self.x_set = False
            self.y_set = True

        # Check for collision along the y axis and have all planes turn right if true
        if self.y_set and (self.y_o == airplane.position.y - (self.y_distance - 1)):
            if (self.heading == Heading.NORTH):
                self.heading = Heading.EAST
            elif (self.heading == Heading.SOUTH):
                self.heading = Heading.WEST
            self.x_set = True
            self.y_set = False

    # Function to update values for airplanes on clock
    def trigger_update(self, airplane: Airplane):
        # Update plane position
        airplane.heading = self.heading
        # if self.x_set:
        #     airplane.position.x = self.x_distance
        #     self.x_set = False
        # elif self.y_set:
        #     airplane.position.y = self.y_distance
        #     self.y_set = False
        



