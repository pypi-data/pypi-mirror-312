from typing import Optional, Dict, Union
from redis.asyncio import Redis
from loguru import logger


class BotSettings:
    """
    Singleton class for managing bot settings stored in Redis.
    Provides methods to initialize, update, and retrieve settings.
    """
    _instance: Optional["BotSettings"] = None
    settings: Dict[str, Union[bool, str]] = {}
    redis: Optional[Redis] = None

    def __new__(cls) -> "BotSettings":
        """
        Ensures that only one instance of BotSettings exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, redis_instance: Redis) -> None:
        """
        Initializes the BotSettings instance with a Redis connection and loads all settings.

        Args:
            redis_instance (Redis): An instance of Redis client.

        Raises:
            ValueError: If the provided Redis instance is None.
        """
        if not redis_instance:
            raise ValueError("Redis instance is required for initializing bot settings.")
        self.redis = redis_instance
        logger.success("Initializing bot settings from Redis...")
        await self.update_all()
        self._log_all_settings()
        logger.info(f"Current settings: {self.settings}")

    async def update_all(self) -> None:
        """
        Updates all bot settings from Redis and stores them in the settings dictionary.

        Raises:
            RuntimeError: If Redis instance is not initialized.
        """
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        keys = await self.redis.keys("bot_setting:*")
        for key in keys:
            value = await self.redis.get(key)
            self._set_setting(key, value)
        logger.success("All settings updated.")

    async def update(self, key: str) -> None:
        """
        Updates a specific bot setting from Redis and stores it in the settings dictionary.

        Args:
            key (str): The key of the setting to update.

        Raises:
            RuntimeError: If Redis instance is not initialized.
        """
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        redis_key = f"bot_setting:{key}"
        value = await self.redis.get(redis_key)
        self._set_setting(redis_key, value)
        logger.success(f"Setting '{key}' updated.")

    def _set_setting(self, key: str, value: str) -> None:
        """
        Parses and sets a setting in the settings dictionary.

        Args:
            key (str): The Redis key of the setting.
            value (str): The value of the setting.
        """
        if value == "0":
            self.settings[key] = False
        elif value == "1":
            self.settings[key] = True
        else:
            self.settings[key] = value

    def _log_all_settings(self) -> None:
        """
        Logs all settings currently loaded in the instance.
        """
        logger.info("Logging all settings:")
        for key, value in self.settings.items():
            logger.info(f"{key}: {value}")

    def __getattr__(self, name: str) -> Union[bool, str]:
        """
        Dynamically retrieves a setting value.

        Args:
            name (str): The name of the setting to retrieve.

        Returns:
            Union[bool, str]: The value of the setting, or False if the setting is not found.
        """
        redis_key = f"bot_setting:{name}"
        return self.settings.get(redis_key, False)


bot_settings = BotSettings()

__all__ = ["bot_settings"]
