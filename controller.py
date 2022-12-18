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
    num_airplanes: int                  # Number of airplanes in list (int)
    distance: list          # Coordinate objects representing the distance left to travel in each respective axis (list of Coordinates)
    next_position: list     # The coordiantes of the plane 1 time step after the heading is set by the controller (list of Coordinates)
    midpoint: list          # Midpoints of the flights of the airplanes to know when to start descent (list of ints)
    z_navigation: list      # Whether or not the plane will be changing altitude to avoid collisions rather than just the 2D directions (list of Bools)

    # Class methods
    # Initialize the controller with the airplanes it is controlling
    def __init__(self, airplane: list) -> None:
        self.airplane = airplane
        self.num_airplanes = len(self.airplane)
        self.distance = [Coordinate] * self.num_airplanes
        self.next_position = [Coordinate] * self.num_airplanes
        self.midpoint = [Coordinate] * self.num_airplanes
        self.z_navigation = [False] * self.num_airplanes
        for ID in range(0,self.num_airplanes):
            self.calculate_midpoint(ID)

    # Function to calculate the midpoint of the flight to know when to start descending
    def calculate_midpoint(self, ID):
        distance = Coordinate(self.airplane[ID].destination.x - self.airplane[ID].position.x,self.airplane[ID].destination.y - self.airplane[ID].position.y,0)

        # If the distance is even, normal case
        if ((abs(distance.x) + abs(distance.y)) % 2 == 0):
            self.midpoint[ID] = (abs(distance.x) + abs(distance.y))/2

        # If the distance is odd, special case to handle to ensure plane levels off around the 2 mid points (signified by negative midpoint)
        else:
            self.midpoint[ID] = -1 * (abs(distance.x) + abs(distance.y))/2

    # Function to calculate the distance the airplane needs to travel in each axis
    def calculate_distance(self, ID):
        self.distance[ID].x = self.airplane[ID].destination.x - self.airplane[ID].position.x
        self.distance[ID].y = self.airplane[ID].destination.y - self.airplane[ID].position.y

    # Function to calculate the position of the aircraft at the next time step (in 1 minute)
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

        # Calculate the plane's next position based on the new heading
        self.calculate_next_position(ID)

    # Function to calculate the altitude of the plane
    def calculate_altitude(self, ID):
        # If the plane needs to change altitude to avoid collision, dive to avoid other planes
        if (self.z_navigation[ID] == True):
            self.airplane[ID].position.z = self.airplane[ID].position.z - 1
            self.z_navigation[ID] = False

        # Check if the plane has reached the midpoint of the flight. If the flight distance was odd, special case (negative midpoint)
        elif (self.midpoint[ID] < 0):

            # If the plane is before the midpoint (level off zone in this case), climb
            if (abs(self.distance[ID].x) + abs(self.distance[ID].y) > (self.midpoint[ID] * -1) + 1) and (self.airplane[ID].position.z < 11):
                self.airplane[ID].position.z = self.airplane[ID].position.z + 1

            # If the plane is past the midpoint (level off zone in this case), descend
            elif (abs(self.distance[ID].x) + abs(self.distance[ID].y) <= (self.midpoint[ID] * -1) - 1)and (self.airplane[ID].position.z >= 0):
                self.airplane[ID].position.z = self.airplane[ID].position.z - 1

        # If the plane is before the midpoint, climb
        elif (abs(self.distance[ID].x) + abs(self.distance[ID].y) > self.midpoint[ID]) and (self.airplane[ID].position.z < 11):
            self.airplane[ID].position.z = self.airplane[ID].position.z + 1

        # If the plane is past the midpoint, descend
        elif (abs(self.distance[ID].x) + abs(self.distance[ID].y) <= self.midpoint[ID]) and (self.airplane[ID].position.z >= 0):
            self.airplane[ID].position.z = self.airplane[ID].position.z - 1

    # Function to check for possible collisions
    def check_for_collision(self, ID):
        # Check to see there are planes further down the list to check
        if (ID + 1 < self.num_airplanes):
            tries = 0

            # Use while loop instead of for..in loop so I can change the iterator value dynamically
            i = ID + 1
            while (i < self.num_airplanes):

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
                    tries = tries + 1

                    # If the heading calculation has happened 4 times, all 2D directions are exhausted. Z (altitude) must change
                    if (tries == 4):
                        self.z_navigation[i] = True
                        self.calculate_altitude(i)
                i = i + 1

    # Run one time step of the controller logic (logic for navigation for the next minute)
    def calculate_next_maneuver(self, airplane: list):
        # Receive inputs of plane locations
        self.airplane = airplane
        self.num_airplanes = len(airplane)

        # Use while loop instead of for..in loop so I can change the iterator value dynamically
        i = 0
        while i < self.num_airplanes:

            # If the plane has landed, remove it from the list
            if self.airplane[i].position is None:
                del self.airplane[i]
                self.num_airplanes = self.num_airplanes - 1

            # Otherwise, calculate the distance to go and heading to follow for each plane
            else:
                self.calculate_distance(i)
                self.calculate_altitude(i)
                self.calculate_heading(i)
                i = i + 1

        # Check for collisions AFTER new headings have been calculated
        for ID in range(0,self.num_airplanes):
            self.check_for_collision(ID)

        # Send outputs (new headings) to planes
        return self.airplane