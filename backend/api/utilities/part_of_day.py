import enum

class Part_Of_Day(enum.Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4
    INVALID_HOUR = 5