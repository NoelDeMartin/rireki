from enum import Enum


class RetentionPolicy(Enum):
    NONE = 'none'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    @classmethod
    def from_string(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None
