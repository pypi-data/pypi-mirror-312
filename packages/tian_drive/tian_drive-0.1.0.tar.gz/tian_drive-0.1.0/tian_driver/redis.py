import os
import shelve

from typing import List, Optional
from tian_drivers.src.driver import Driver
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple

import redis

class Redis(Driver):
    def __init__(
        self,
        url: str= None
    ):
        #logger.debug(f"Redis storage dir: {storage_dir}")

        super().__init__()
        self.client = redis.Redis.from_url(url)
        print("PING REDIS: ", self.client.ping())


    def set_value(self, key, value, ttl):
        """Set a value in the Redis store."""
        return self.client.set(key, value, ttl)

    def get_value(self, key):
        """Get a value from the Redis store."""
        return self.client.get(key)

    def delete_value(self, key):
        """Delete a value from the Redis store."""
        self.client.delete(key)

    def exists(self, key):
        """Check if a key exists in the Redis store."""
        return self.client.exists(key)

    def increment(self, key, amount=1):
        """Increment the integer value of a key by the given amount."""
        return self.client.incr(key, amount)

    def decrement(self, key, amount=1):
        """Decrement the integer value of a key by the given amount."""
        return self.client.decr(key, amount)

    def set_expiry(self, key, time):
        """Set an expiry time on a key."""
        self.client.expire(key, time)

    def query(self, **kwargs) -> List[Tuple]:
        """Execute a query that returns many records"""
        raise NotImplementedError('query method is not implemented for RedisClient')

    def query_one(self, **kwargs) -> Any:
        """Execute a query that returns just one record"""
        raise NotImplementedError('query_one method is not implemented for RedisClient')

    def query_none(self, **kwargs) -> NoReturn:
        """Execute a query that doesn't return any record"""
        raise NotImplementedError('query_none method is not implemented for RedisClient')

    def commit(self) -> NoReturn:
        """Commit transaction on DB to persist operations."""
        # Redis doesn't use transactions like SQL databases, so this may be a no-op
        pass

    def rollback(self) -> NoReturn:
        """Rollback failure operation."""
        # Redis doesn't use transactions like SQL databases, so this may be a no-op
        pass

    def close(self) -> NoReturn:
        """Close current connection."""
        self.client.close()

    def get_real_driver(self) -> Any:
        """Return the current real driver instance."""
        return self.client

    def placeholder(self, **kwargs) -> AnyStr:
        """Return the next driver placeholder for prepared statements"""
        # Redis doesn't use placeholders like SQL databases
        return ""

    def reset_placeholder(self) -> NoReturn:
        """This method is used to reset numeric based placeholders."""
        # Redis doesn't use placeholders like SQL databases
        pass

    def execute(self, sql: AnyStr, *args) -> NoReturn:
        """Execute a query that doesn't return any record"""
        raise NotImplementedError('execute method is not implemented for RedisClient')

