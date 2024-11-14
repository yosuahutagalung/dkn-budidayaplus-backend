import enum

class TaskStatus(enum.Enum):
    TODO = "TODO"
    DONE = "DONE"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class TaskType(enum.Enum):
    POND_QUALITY = "POND_QUALITY"
    FISH_SAMPLING = "FISH_SAMPLING"
    FOOD_SAMPLING = "FOOD_SAMPLING"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
