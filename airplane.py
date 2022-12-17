#   airplane.py
#
#   Author: Ethan Mayer
#   Fall 2022
#
#   This file contains the classes required for the controller to function, such as the Heading object, Coordiante object, and Airplane object.

# Includes
from enum import Enum
from copy import deepcopy

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
    #
    # def __new__(cls: type[Self]) -> Self:
    #     pass
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

    # Define != behavior
    def __ne__(self, __o: object) -> bool:
        return self.x != __o.x or self.y != __o.y or self.z != __o.z

# Class for the airplane
class Airplane:
    # Class variables
    identifier: chr                                 # Identifier to be printed on the map
    origin: Coordinate = Coordinate(0, 0, 0)        # Starting location of airplane
    destination: Coordinate = Coordinate(0, 0, 0)   # Landing location of airplane
    position: Coordinate = Coordinate(0, 0, 0)      # Current location of airplane
    heading: Heading = Heading.NORTH                # Current heading of airplane
    speed: int = 1                                  # Current speed of airplane (constant 1km/s)

    # Class methods
    # Initialize the airplane with origin location and destination location
    def __init__(self, id, origin, destination) -> None:
        self.identifier = id
        self.origin = origin
        self.destination = destination
        self.position = deepcopy(self.origin)

    # String formatting for printing
    def __str__(self) -> str:
        if self.position is None:
            return f"Plane arrived at {self.destination}"
        else:
            return f"Plane @ {self.position} heading {self.heading.name} toward {self.destination} @ speed 1"

    # String formatting for printing in lists
    def __repr__(self) -> str:
        return f"Plane @ {self.position}"

    # Update the plane's position using heading input received from the centralized controller
    def run(self):
        # If the plane has not arrived at the destination, follow the heading given by the flight controller
        if (self.position != self.destination):
            if (self.heading == Heading.EAST):
                self.position.x = self.position.x + self.speed
            elif (self.heading == Heading.WEST):
                self.position.x = self.position.x - self.speed
            elif (self.heading == Heading.NORTH):
                self.position.y = self.position.y + self.speed
            elif (self.heading == Heading.SOUTH):
                self.position.y = self.position.y - self.speed
        # If the plane has landed, set position to none to stop reporting current location
        else:
            self.position = None

