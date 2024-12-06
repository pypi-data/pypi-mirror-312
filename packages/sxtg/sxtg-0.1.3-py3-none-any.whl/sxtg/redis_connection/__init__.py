from typing import Optional
import redis.asyncio as aioredis
from loguru import logger


class RedisConnection:
    """
    Singleton class for managing a Redis connection.
    Provides methods to initialize, close, and interact with Redis.
    """
    _instance: Optional["RedisConnection"] = None
    connection: Optional[aioredis.Redis] = None

    def __new__(cls, *args, **kwargs) -> "RedisConnection":
        """
        Ensures that only one instance of RedisConnection exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    async def initialize(self, redis_url: str) -> None:
        """
        Initializes the Redis connection using the provided URL.

        Args:
            redis_url (str): The Redis connection URL.

        Raises:
            Exception: If the connection to Redis fails.
        """
        if self.connection is None:
            try:
                logger.info("Connecting to Redis...")
                self.connection = await aioredis.from_url(
                    redis_url, decode_responses=True
                    )
                # Test connection
                await self.connection.ping()
                logger.success("Redis connection established.")
            except Exception as e:
                self.connection = None
                logger.error(f"Failed to connect to Redis: {e}")
                raise

    async def close(self) -> None:
        """
        Closes the Redis connection if it is open.

        Raises:
            Exception: If an error occurs while closing the connection.
        """
        if self.connection:
            try:
                await self.connection.close()
                logger.info("Redis connection closed.")
            except Exception as e:
                logger.error(f"Error while closing Redis connection: {e}")

    def __getattr__(self, name):  # type: ignore
        """
        Delegates attribute access to the Redis connection instance.

        Args:
            name (str): The attribute name to access.

        Returns:
            Any: The attribute from the Redis connection.

        Raises:
            AttributeError: If the Redis connection is not initialized.
        """
        if not self.connection:
            raise AttributeError("Redis connection is not initialized.")
        return getattr(self.connection, name)  # type: ignore


redis = RedisConnection()

__all__ = ["redis"]
