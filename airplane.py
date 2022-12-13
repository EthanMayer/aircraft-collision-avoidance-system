#   airplane.py
#
#   Author: Ethan Mayer
#   Fall 2022

# Includes
from enum import Enum

# Class for the airplane's heading
class Heading(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270

# Class for the airplane's coordinates
class Coordinate:
    # Class variables
    x: int
    y: int
    z: int

    # Class methods
    # Initialize coordinate with x, y, and z positions
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    # String formatting for printing
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    # Define == behavior
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

# Class for the airplane
class Airplane:
    # Class variables
    origin: Coordinate = Coordinate(0, 0, 0)
    destination: Coordinate = Coordinate(0, 0, 0)
    position: Coordinate = Coordinate(0, 0, 0)
    heading: Heading = Heading.NORTH
    speed: int = 1

    # Class methods
    # Initialize the airplane with origin location and destination location
    def __init__(self, origin, destination) -> None:
        self.origin = origin
        self.destination = destination
        self.position = self.origin

    # String formatting for printing
    def __str__(self) -> str:
        if (self.position != self.destination):
            return f"Plane @ {self.position} heading {self.heading.name} toward {self.destination} @ speed 1"
        else:
            return f"Plane arrived at {self.destination}"

    # String formatting for printing in lists
    def __repr__(self) -> str:
        return f"Plane @ {self.position}"

    # Update the plane's position using heading received from the centralized controller
    def run(self):
        if (self.position != self.destination):
            if (self.heading == Heading.EAST):
                self.position.x = self.position.x + self.speed
            elif (self.heading == Heading.WEST):
                self.position.x = self.position.x - self.speed
            elif (self.heading == Heading.NORTH):
                self.position.y = self.position.y + self.speed
            elif (self.heading == Heading.SOUTH):
                self.position.y = self.position.y - self.speed
