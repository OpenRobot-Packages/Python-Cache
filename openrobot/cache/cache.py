import typing
import asyncio
import datetime
import aioredis, redis as sync_redis
from .enums import *
from .error import *

class Cache:
    """The base Cache class.
    
    Parameters
    ----------
    redis: Optional[Union[:class:`aioredis.client.Redis`, :class:`redis.Redis`]]
        The redis client to cache with.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The asyncio loop to be used. Defaults to :meth:`asyncio.get_event_loop`.
    """

    def __init__(self, redis: typing.Optional[typing.Union[aioredis.Redis, sync_redis.Redis]] = None, *, loop: asyncio.AbstractEventLoop = None):
        self._redis: typing.Union[aioredis.Redis, sync_redis.Redis] = redis if isinstance(redis, (aioredis.Redis, sync_redis.Redis)) else None
        self._cache_type: CacheType = CacheType.AsyncRedis if isinstance(self._redis, aioredis.Redis) else CacheType.SyncRedis if isinstance(self._redis, sync_redis.Redis) else CacheType.Dict

        self._cache: dict = {} if self._cache_type is CacheType.Dict else None

        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()

        self._is_redis_sync = None if not self._redis else isinstance(self.redis, aioredis.Redis)

    @property
    def redis(self) -> typing.Union[aioredis.Redis, None]:
        """:class:`aioredis.client.Redis`: The redis client that is being used to cache,"""
        return self._redis

    @redis.setter
    async def redis_setter(self, value):
        if not isinstance(value, aioredis.Redis, sync_redis.Redis):
            raise UnexpectedType(['aioredis.Redis', 'redis.Redis'], value)

        self._redis = value

        self._cache_type = CacheType.AsyncRedis if isinstance(self._redis, aioredis.Redis) else CacheType.SyncRedis if isinstance(self._redis, sync_redis.Redis) else CacheType.Dict

        self._is_redis_sync = None if not self._redis else isinstance(self._redis, aioredis.Redis)

    @property
    def cache_type(self) -> CacheType:
        """:class:`CacheType`: The cache type."""
        return self._cache_type

    @cache_type.setter
    def cache_type_setter(self, value):
        if not isinstance(value, CacheType):
            raise UnexpectedType(CacheType, value)

        self._cache_type = value

    def cache(self):
        """|maybecoro|
        
        Gets all the cache.
        
        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis`, then
        this function would be a coroutine. Else, it will return
        a :class:`dict`.

        Returns
        -------
        :class:`dict`
            All the cache found.
        """
        
        if self._cache_type is CacheType.Dict:
            return self._cache
        elif self._cache_type is CacheType.SyncRedis:
            d = {}

            keys = self._redis.keys()

            for key in keys:
                d[key.decode()] = (self._redis.get(key.decode())).decode()
        elif self.cache_type is CacheType.AsyncRedis:
            async def _cache():
                d = {}

                keys = await self._redis.keys()

                for key in keys:
                    d[key.decode()] = (await self._redis.get(key.decode())).decode()

                return d

            return _cache

    def get(self, key: typing.Union[str, typing.Any]):
        """|maybecoro|
        
        Gets the value from the key provided.

        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis`, then
        this function would be a coroutine. Else, it will return
        a :class:`typing.Any`.

        Parameters
        ----------
        key: Union[:class:`str`, :class:`Any`]
            The value's key to get.

        Returns
        -------
        Optional[Union[:class:`str`, :class:`Any`]]
            The value of the key. `None` if not found.
        """
        
        if self._cache_type is CacheType.Dict:
            return self._cache.get(key)
        elif self._cache_type is CacheType.SyncRedis:
            x = self._redis.get()
            return getattr(x, 'decode', lambda: x)()
        elif self._cache_type is CacheType.AsyncRedis:
            async def _get() -> str:
                x = await self._redis.get(key.decode())

                if x is None:
                    return None

                return x.decode()

            return _get

    def keys(self):
        """|maybecoro|

        Returns a list of keys.

        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis`, then
        this function would be a coroutine. Else, it will return
        a :class:`typing.Any`.

        Returns
        -------
        List[Union[:class:`str`, :class:`Any`]]
            The list of keys in the cache.
        """
        
        if self._cache_type is CacheType.Dict:
            return list(self._cache.keys())
        elif self._cache_type is CacheType.SyncRedis:
            return [key.decode() for key in self._redis.keys()]
        elif self._cache_type is CacheType.AsyncRedis:
            async def _keys() -> typing.List[str]:
                return [getattr(key, 'decode', lambda: key)() for key in await self._redis.keys()]

            return _keys

    def values(self):
        """|maybecoro|

        Returns a list of values.

        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis`, then
        this function would be a coroutine. Else, it will return
        a :class:`typing.Any`.

        Returns
        -------
        List[Union[:class:`str`, :class:`Any`]]
            The list of values in the cache.
        """

        if self._cache_type is CacheType.Dict:
            return list(self._cache.values())
        elif self._cache_type is CacheType.SyncRedis:
            l = []

            for key in self._redis.keys:
                x = self._redis.get(getattr(key, 'decode', lambda: key)())

                l.append(getattr(x, 'decode', lambda: x)())

            return l
        elif self._cache_type is CacheType.AsyncRedis:
            async def _values():
                return [(await self._redis.get(key.decode())).decode() for key in await self._redis.keys()]

            return _values

    def set(self, key: typing.Union[str, bytes, memoryview, typing.Any], value: typing.Union[str, int, float, bytes, memoryview, typing.Any], *, delete_after: typing.Union[datetime.timedelta, int, float] = None):
        """|maybecoro|

        Set a key and value to the cache.

        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis`, then
        this function would be a coroutine. 

        Parameters
        ----------
        key: Union[:class:`str`, :class:`bytes`, :class:`memoryview`, :class:`Any`]
            The key to be set.
        value: Union[:class:`str`, :class:`int`, :class:`float`, :class:`bytes`, :class:`memoryview`, :class:`Any`]
            The value to be set.
        delete_after: Union[:class:`datetime.timedelta`, :class:`int`, :class:`float`]
            When to delete the key. Either a :class:`datetime.timedelta` is accepted, or a :class:`int`/:class:`float`
            is accepted which will represent the amount of seconds until deletion.

        Raises
        ------
        :exc:`.UnexpectedType`
            An unexpected type argument was given.
        """
        
        if self._cache_type is CacheType.Dict:
            self._cache[key] = value

            async def delete_task():
                await asyncio.sleep(getattr(delete_after, 'total_seconds', lambda: delete_after)())

                try:
                    del self._cache[key]
                except:
                    pass

            if self.loop:
                self.loop.create_task(delete_task())
        elif self._cache_type is CacheType.SyncRedis:
            self._redis.set(key, value, delete_after)
        elif self._cache_type is CacheType.AsyncRedis:
            if not isinstance(key, (str, bytes, memoryview)):
                raise UnexpectedType([str, bytes, memoryview], key)

            if not isinstance(value, (str, int, float, bytes, memoryview)):
                raise UnexpectedType([str, int, float, bytes, memoryview], value)

            self._redis.set(key, value, delete_after)

    def clear(self, all: bool = False):
        """|maybecoro|

        Clears all the items in the cache.

        If :meth:`.cache_type` is :class:`CacheType.AsyncRedis` or `all` is True
        and :meth:`.redis` is an instance of :class:`aioredis.client.Redis`, then
        this function would be a coroutine.

        Parameters
        ----------
        all: Optional[:class:`bool`]
            Clears **all** the cache from **all the cache methods provided (both Redis and local)**.

        Returns
        -------
        :class:`dict`:
            The list of keys and values stored in the cache.
        ``None``:
            `None` is returned if ``all`` is True. 
        """

        if all:
            if isinstance(self._redis, aioredis.Redis):
                async def _clear():
                    self._cache = {}

                    await self._redis.flushdb()

                return _clear
            elif isinstance(self._redis, sync_redis.Redis):
                self._cache = {}

                self._redis.flushdb()

            return
        else:
            d = self.cache()
            if self._cache_type is CacheType.Dict:
                self._cache = {}
            elif self._cache_type is CacheType.SyncRedis:
                self._redis.flushdb()
            elif self._cache_type is CacheType.AsyncRedis:
                async def _clear():
                    await self._redis.flushdb()

                    return d

                return _clear

            return d