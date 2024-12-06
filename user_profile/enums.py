import enum

class Role(enum.Enum):
    WORKER = "worker"
    SUPERVISOR = "supervisor"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
