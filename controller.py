#   controller.py
#
#   Author: Ethan Mayer
#   Fall 2022

# Includes
from airplane import *

# Class for the centralized aircraft controller
class Controller:
    # Class variables
    airplane: list
    #airplane: Airplane
    x_distance: list
    y_distance: list
    z_distance: list
    # heading = list()
    x_set: list
    y_set: list
    x_o: int = 0 # TODO: Temporary other airplane coordinate
    y_o: int = 0 # TODO: Temporary other airplane coordinate

    # Class methods
    # Initialize the controller with the airplanes it is controlling
    def __init__(self, airplane: list) -> None:
        self.airplane = airplane
        n = len(self.airplane)
        self.x_distance = [int] * n
        self.y_distance = [int] * n
        self.z_distance = [int] * n
        self.x_set = [False] * n
        self.y_set = [False] * n

    # Function to calculate the distance the airplane needs to travel
    def calculate_distance(self, ID):
        origin = self.airplane[ID].origin
        destination = self.airplane[ID].destination
        self.x_distance[ID] = destination.x - origin.x
        self.y_distance[ID] = destination.y - origin.y
        # self.z_distance TODO: Altitude calculations

    # Function to calculate the heading the plane needs to use
    def calculate_heading(self, ID):
        # Traverse either x axis or y axis one at a time, prioritizing x axis
        if not self.y_set[ID]:
            if (self.x_distance[ID] > 0):
                self.airplane[ID].heading = Heading.EAST
                self.x_set[ID] = True
            elif (self.x_distance[ID] < 0):
                self.airplane[ID].heading = Heading.WEST
                self.x_set[ID] = True
        if not self.x_set[ID]:
            if (self.y_distance[ID] > 0):
                self.airplane[ID].heading = Heading.NORTH
                self.y_set[ID] = True
            elif (self.y_distance[ID] < 0):
                self.airplane[ID].heading = Heading.SOUTH
                self.y_set[ID] = True


    # Function to check for possible collisions
    def check_for_collision(self, ID):
        # # Check for collision along the x axis and have all planes turn right if true
        # if self.x_set[1] and (abs(self.airplane[1].position.x - self.airplane[0].position.x) <= 2):
        #     if (self.airplane[1].heading == Heading.EAST):
        #         self.airplane[1].heading = Heading.SOUTH
        #     elif (self.airplane[1].heading == Heading.WEST):
        #         self.airplane[1].heading = Heading.NORTH
        #     self.x_set[1] = False
        #     self.y_set[1] = True

        # # Check for collision along the y axis and have all planes turn right if true
        # elif self.y_set[1] and (abs(self.airplane[1].position.x - self.airplane[0].position.y) <= 2):
        #     if (self.airplane[1].heading == Heading.NORTH):
        #         self.airplane[1].heading = Heading.EAST
        #     elif (self.airplane[1].heading == Heading.SOUTH):
        #         self.airplane[1].heading = Heading.WEST
        #     self.x_set[1] = True
        #     self.y_set[1] = False
        if (abs(self.airplane[1].position.x - self.airplane[0].position.x) <= 2) and (abs(self.airplane[1].position.y - self.airplane[0].position.y) <= 2):
            if (self.airplane[1].heading == Heading.NORTH):
                self.airplane[1].heading = Heading.EAST
            elif (self.airplane[1].heading == Heading.EAST):
                self.airplane[1].heading == Heading.SOUTH
            elif (self.airplane[1].heading == Heading.SOUTH):
                self.airplane[1].heading == Heading.WEST
            else:
                self.airplane[1].heading = Heading.NORTH
            # self.x_set[1] = False
            # self.y_set[1] = True

    # Function to update values for airplanes on clock
    def trigger_update(self, airplane: Airplane):
        # Update plane position
        airplane.heading = self.heading
        self.x_set = False
        self.y_set = False
        # if self.x_set:
        #     airplane.position.x = self.x_distance
        #     self.x_set = False
        # elif self.y_set:
        #     airplane.position.y = self.y_distance
        #     self.y_set = False

    # Run one time step of the controller logic
    def run(self, airplane: list):
        n = len(airplane)
        for ID in range(0,n):
            self.airplane = airplane
            self.calculate_distance(ID)
            self.calculate_heading(ID)
            self.check_for_collision(ID)
            self.x_set[ID] = False
            self.y_set[ID] = False
            #self.trigger_update(self.airplane)
        return self.airplane