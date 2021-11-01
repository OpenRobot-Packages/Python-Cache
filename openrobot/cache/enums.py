import enum

class Enum(enum.Enum):
    def __str__(self) -> str:
        return self.name

class CacheType(Enum):
    AsyncRedis = 0
    SyncRedis = 1
    Dict = 2