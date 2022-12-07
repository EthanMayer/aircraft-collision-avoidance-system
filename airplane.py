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
    x: int
    y: int
    z: int

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

# Class for the airplane
class Airplane:
    origin: Coordinate = Coordinate(0, 0, 0)
    destination: Coordinate = Coordinate(0, 0, 0)
    position: Coordinate = Coordinate(0, 0, 0)
    heading: Heading
    speed: int = 1

    def __init__(self, origin, destination) -> None:
        self.origin = origin
        self.destination = destination
        self.position = self.origin

    def __str__(self) -> str:
        return f"Plane @ {self.position} heading {self.heading} toward {self.destination}"
