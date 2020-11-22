from enum import Enum


# Stores the parsing status for a current cell
class LineStatus(Enum):
    TEXT = 1
    SOLUTION = 2
    TASK = 3
