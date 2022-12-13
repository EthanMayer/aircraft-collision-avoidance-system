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
    n: int
    x_distance: list
    y_distance: list
    z_distance: list
    x_set: list
    y_set: list

    # Class methods
    # Initialize the controller with the airplanes it is controlling
    def __init__(self, airplane: list) -> None:
        self.airplane = airplane
        self.n = len(self.airplane)
        self.x_distance = [int] * self.n
        self.y_distance = [int] * self.n
        self.z_distance = [int] * self.n
        self.x_set = [False] * self.n
        self.y_set = [False] * self.n

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
        if (ID < self.n - 1):
            for i in range(ID + 1, self.n):
                if (abs(self.airplane[ID].position.x - self.airplane[i].position.x) <= 2) and (abs(self.airplane[ID].position.y - self.airplane[i].position.y) <= 2):
                    if (self.airplane[i].heading == Heading.NORTH):
                        self.airplane[i].heading = Heading.EAST
                    elif (self.airplane[i].heading == Heading.EAST):
                        self.airplane[i].heading == Heading.SOUTH
                    elif (self.airplane[i].heading == Heading.SOUTH):
                        self.airplane[i].heading == Heading.WEST
                    else:
                        self.airplane[i].heading = Heading.NORTH


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
        for ID in range(0,self.n):
            self.airplane = airplane
            self.calculate_distance(ID)
            self.calculate_heading(ID)
            self.x_set[ID] = False
            self.y_set[ID] = False
        for ID in range(0,self.n):
            self.check_for_collision(ID)
        return self.airplane