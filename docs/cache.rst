.. currentmodule:: openrobot.cache

OpenRobot Cache Documentation
=============================

Cache
-----

Cache
~~~~~

.. autoclass:: Cache
    :members:
    :exclude-members: redis_setter, cache_type_setter

Enums
-----

CacheType
~~~~~~~~~

.. class:: openrobot.cache.CacheType

    Specifies the Cache Type.

    .. attribute:: AsyncRedis

        Async Redis Cache Type.
    .. attribute:: SyncRedis

        Sync Redis Cache Type.
    .. attribute:: Dict

        Dict Cache Type.

Error
-----

.. autoexception:: OpenRobotCacheException

.. autoexception:: UnexpectedType