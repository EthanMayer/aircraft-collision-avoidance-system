#   controller.py
#
#   Author: Ethan Mayer
#   Fall 2022
#
#   This file contains the aircraft controller. This controller can handle routing an arbitrary amount of planes to their destinations in 3D while avoiding collisions.

# Includes
from airplane import *
from copy import deepcopy

# Class for the centralized aircraft controller
class Controller:
    # Class variables
    airplane: list      # Airplanes the controller is interfacing with (list of airplanes)
    n: int              # Number of airplanes in list
    x_distance: list    # X distance left to travel for each plane (list of ints)
    y_distance: list    # Y distance left to travel for each plane (list of ints)
    # z_distance: list    # Z distance left to travel for each plane (list of ints)
    x_set: list         # If the plane is traveling the X distance (list of bools)
    y_set: list         # If the plane is traveling the Y distance (list of bools)
    next_position: list # The coordiantes of the plane 1 time step after the heading is set by the controller (list of Coordinates)

    # Class methods
    # Initialize the controller with the airplanes it is controlling
    def __init__(self, airplane: list) -> None:
        self.airplane = airplane
        self.n = len(self.airplane)
        self.x_distance = [int] * self.n
        self.y_distance = [int] * self.n
        # self.z_distance = [int] * self.n
        self.x_set = [False] * self.n
        self.y_set = [False] * self.n
        self.next_position = [Coordinate] * self.n

    # Function to calculate the distance the airplane needs to travel in each axis
    def calculate_distance(self, ID):
        self.x_distance[ID] = self.airplane[ID].destination.x - self.airplane[ID].position.x
        self.y_distance[ID] = self.airplane[ID].destination.y - self.airplane[ID].position.y

    # Function to calculate the position of the aircraft at the next time step (in 1 hr)
    def calculate_next_position(self, ID):
        # Grab the current position
        self.next_position[ID] = deepcopy(self.airplane[ID].position)

        # Calculate the next position based on the current heading of the plane
        if (self.airplane[ID].heading == Heading.EAST):
            self.next_position[ID].x = self.airplane[ID].position.x + self.airplane[ID].speed
        if (self.airplane[ID].heading == Heading.WEST):
            self.next_position[ID].x = self.airplane[ID].position.x - self.airplane[ID].speed
        if (self.airplane[ID].heading == Heading.NORTH):
            self.next_position[ID].y = self.airplane[ID].position.y + self.airplane[ID].speed
        if (self.airplane[ID].heading == Heading.SOUTH):
            self.next_position[ID].y = self.airplane[ID].position.y - self.airplane[ID].speed

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
        self.calculate_next_position(ID)

    # Function to calculate the altitude of the plane
    def calculate_altitude(self, ID):
        # The plane climbs 10 km to cruising altitude within an hour of takeoff
        if (self.airplane[ID].position == self.airplane[ID].origin):
            self.airplane[ID].position.z = 10
        # The plane decends to 0 km in 1 hr (1 timestep) to land when reaching its destination
        elif (self.next_position[ID].x == self.airplane[ID].destination.x) and (self.next_position[ID].y == self.airplane[ID].destination.y):
            self.airplane[ID].position.z = 0

    # Function to check for possible collisions
    def check_for_collision(self, ID):
        # Check to see there are planes further down the list to check
        if (ID + 1 < self.n):
            i = ID + 1
            t = 0
            # Use while loop instead of for..in loop so I can change the iterator value dynamically
            while (i < self.n):
                # Check if a collision will occur within the next move
                if (self.next_position[ID] == self.next_position[i]) or (self.airplane[ID].position == self.next_position[i]):

                    # If collision will occur, turn the higher ID plane right 90 degrees
                    if (self.airplane[i].heading == Heading.NORTH):
                        self.airplane[i].heading = Heading.EAST
                    elif (self.airplane[i].heading == Heading.EAST):
                        self.airplane[i].heading == Heading.SOUTH
                    elif (self.airplane[i].heading == Heading.SOUTH):
                        self.airplane[i].heading == Heading.WEST
                    else:
                        self.airplane[i].heading = Heading.NORTH

                    # Calculate the next position based on the new heading
                    self.calculate_next_position(i)
                    i = i - 1
                    t = t + 1

                    # If the heading calculation has happened 4 times, all 2D directions are exhausted. Z (altitude) must change
                    if (t == 4):
                        pass
                i = i + 1


    # # Function to update values for airplanes on clock
    # def trigger_update(self, airplane: Airplane):
    #     # Update plane position
    #     airplane.heading = self.heading
    #     self.x_set = False
    #     self.y_set = False
    #     # if self.x_set:
    #     #     airplane.position.x = self.x_distance
    #     #     self.x_set = False
    #     # elif self.y_set:
    #     #     airplane.position.y = self.y_distance
    #     #     self.y_set = False

    # Run one time step of the controller logic
    def run(self, airplane: list):
        # Receive inputs of plane locations
        self.airplane = airplane
        self.n = len(airplane)

        i = 0
        # Use while loop instead of for..in loop so I can change the iterator value dynamically
        while i < self.n:

            # If the plane has landed, remove it from the list
            if self.airplane[i].position is None:
                del self.airplane[i]
                self.n = self.n - 1
            # Otherwise, calculate the distance to go and heading to follow for each plane
            else:
                self.calculate_distance(i)
                self.calculate_heading(i)
                self.calculate_altitude(i)
                self.x_set[i] = False
                self.y_set[i] = False
                i = i + 1

        # Check for collisions AFTER new headings have been calculated
        for ID in range(0,self.n):
            self.check_for_collision(ID)

        # Send outputs (new headings) to planes
        return self.airplane