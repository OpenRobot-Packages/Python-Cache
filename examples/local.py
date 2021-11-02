from openrobot import cache

cls = cache.Cache()

# Get list of cache
cls.cache()

# Cache Type
cls.cache_type # openrobot.cache.CacheType

# Clear all keys
cls.clear()

# Get a key's value
cls.get('my-key')

# Get list of keys
cls.keys()

# Get list of values
cls.values()

# Add/set a key
cls.set('my-key', 'my-value', delete_after=...)