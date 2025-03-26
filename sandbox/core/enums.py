import enum

class SandboxStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    UNKNOWN = "unknown" # Good practice to have a default/unknown state

    # Optional: Add a default value property if needed
    @classmethod
    def default(cls):
        return cls.PENDING