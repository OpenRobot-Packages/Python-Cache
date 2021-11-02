import aioredis
from openrobot import cache

cls = cache.Cache(aioredis.Redis(...))

# Get list of cache
await cls.cache()

# Cache Type
cls.cache_type # openrobot.cache.CacheType

# Clear all keys
await cls.clear()

# Get a key's value
await cls.get('my-key')

# Get list of keys
await cls.keys()

# Get list of values
await cls.values()

# Add/set a key
await cls.set('my-key', 'my-value', delete_after=...)