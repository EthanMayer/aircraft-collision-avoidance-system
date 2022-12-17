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
    airplane: list          # Airplanes the controller is interfacing with (list of airplanes)
    n: int                  # Number of airplanes in list (int)
    distance: list          # Coordinate objects representing the distance left to travel in each respective axis (list of Coordinates)
    next_position: list     # The coordiantes of the plane 1 time step after the heading is set by the controller (list of Coordinates)
    midpoint: list          # Midpoints of the flights of the airplanes to know when to start descent (list of ints)
    z_navigation = False    # Whether or not the plane will be changing altitude to avoid collisions rather than just the 2D directions (Bool)

    # Class methods
    # Initialize the controller with the airplanes it is controlling
    def __init__(self, airplane: list) -> None:
        self.airplane = airplane
        self.n = len(self.airplane)
        self.distance = [Coordinate] * self.n
        self.next_position = [Coordinate] * self.n
        self.midpoint = [Coordinate] * self.n
        for ID in range(0, self.n):
            self.calculate_distance[ID]
            self.calculate_midpoint[ID]

    # Function to calculate the midpoint of the flight to know when to start descending
    def calculate_midpoint(self, ID):
        if (self.distance[ID].x + self.distance[ID].y % 2 == 0):
            self.midpoint[ID] = (self.distance[ID].x + self.distance[ID].y)/2
        else:
            self.midpoint[ID] = -1 * (self.distance[ID].x + self.distance[ID].y)/2
        # # Calculate X midpoint
        # if (self.distance[ID].x % 2 == 0):
        #     self.midpoint[ID].x = self.distance[ID].x/2

        # # If the distance is odd, make it negative so it knows to level off for a few timesteps
        # else:
        #     self.midpoint[ID].x = -1 * self.distance[ID].x/2

        # # Calculate Y midpoint
        # if (self.distance[ID].y % 2 == 0):
        #     self.midpoint[ID].y = self.distance[ID].y/2

        # # If the distance is odd, make it negative so it knows to level off for a few timesteps
        # else:
        #     self.midpoint[ID].y = -1 * self.distance[ID].y/2

    # Function to calculate the distance the airplane needs to travel in each axis
    def calculate_distance(self, ID):
        self.distance[ID].x = self.airplane[ID].destination.x - self.airplane[ID].position.x
        self.distance[ID].y = self.airplane[ID].destination.y - self.airplane[ID].position.y

    # Function to calculate the position of the aircraft at the next time step (in 1 sec)
    def calculate_next_position(self, ID):
        self.calculate_altitude(ID)
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

    # Function to calculate the heading the plane needs to use (one heading is exhausted before changing heading)
    def calculate_heading(self, ID):
        x_set = False

        # Fly along x axis (priority)
        if (self.distance[ID].x > 0):
            self.airplane[ID].heading = Heading.EAST
            x_set = True
        elif (self.distance[ID].x < 0):
            self.airplane[ID].heading = Heading.WEST
            x_set = True

        # Fly along y axis (if x axis is not being traversed)
        if not x_set:
            if (self.distance[ID].y > 0):
                self.airplane[ID].heading = Heading.NORTH
            elif (self.distance[ID].y < 0):
                self.airplane[ID].heading = Heading.SOUTH

        # Calculate the plane's next position based on the new hading
        self.calculate_next_position(ID)

    # Function to calculate the altitude of the plane
    def calculate_altitude(self, ID):
        # If the plane needs to change altitude to avoid collision, dive to avoid other planes
        if (self.z_navigation == True):
            self.airplane[ID].position.z = self.airplane[ID].position.z - 1

        # If the plane is landing, the plane decends to 0 km in 1 hr (1 timestep) to land when reaching its destination and not takeoff again
        elif ((self.next_position[ID].x == self.airplane[ID].destination.x) and (self.next_position[ID].y == self.airplane[ID].destination.y)) or (self.airplane[ID].position == self.airplane[ID].destination):
            self.airplane[ID].position.z = 0

        # Check if the plane has reached the midpoint of the flight. If the flight distance was odd, special case (negative midpoint)
        elif (self.distance[ID].x + self.distance[ID].y < 0):

            # If the plane is before the midpoint (level off zone in this case), climb
            if (self.distance[ID].x + self.distance[ID].y > (self.midpoint[ID] * -1) + 1):
                self.airplane[ID].position.z = self.airplane[ID].position.z + 1

            # If the plane is past the midpoint (level off zone in this case), descend
            elif (self.distance[ID].x + self.distance[ID].y <= (self.midpoint[ID] * -1) - 1):
                self.airplane[ID].position.z = self.airplane[ID].position.z - 1

        # If the plane is before the midpoint, climb
        elif (self.distance[ID].x + self.distance[ID].y > self.midpoint[ID]):
            self.airplane[ID].position.z = self.airplane[ID].position.z + 1

        # If the plane is past the midpoint, descend
        elif (self.distance[ID].x + self.distance[ID].y <= self.midpoint[ID]):
            self.airplane[ID].position.z = self.airplane[ID].position.z - 1

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
                        self.z_navigation = True
                        self.calculate_altitude(i)
                i = i + 1

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
                i = i + 1

        # Check for collisions AFTER new headings have been calculated
        for ID in range(0,self.n):
            self.check_for_collision(ID)

        # Send outputs (new headings) to planes
        return self.airplane