from typing import Optional, Dict
from redis.asyncio import Redis
from loguru import logger
import re
import sys


class TextContent:
    """
    Singleton class for managing text content stored in Redis.
    Provides methods to initialize, update, and retrieve text content.
    """
    _instance: Optional["TextContent"] = None
    texts: Dict[str, str] = {}
    redis: Optional[Redis] = None

    def __new__(cls) -> "TextContent":
        """
        Ensures that only one instance of TextContent exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, redis_instance: Redis) -> None:
        """
        Initializes the TextContent instance with a Redis connection and loads all texts.

        Args:
            redis_instance (Redis): An instance of Redis client.

        Raises:
            ValueError: If the provided Redis instance is None.
        """
        if not redis_instance:
            raise ValueError("Redis instance is required for initializing TextContent.")
        self.redis = redis_instance
        logger.success("Initializing texts from Redis...")
        await self.update_all()
        self._log_all_texts()

    async def update_all(self) -> None:
        """
        Updates all text entries from Redis and validates their formatting.

        Raises:
            RuntimeError: If Redis instance is not initialized.
        """
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        keys = await self.redis.keys("text:*")
        for key in keys:
            text = await self.redis.get(key)
            self.texts[key] = text
            self._check_formatting_errors(key, text)
        logger.success("All texts updated.")

    async def update(self, key: str) -> None:
        """
        Updates a specific text entry from Redis and validates its formatting.

        Args:
            key (str): The key of the text entry to update.

        Raises:
            RuntimeError: If Redis instance is not initialized.
        """
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        redis_key = f"text:{key}"
        text = await self.redis.get(redis_key)
        self.texts[redis_key] = text
        self._check_formatting_errors(redis_key, text)
        logger.success(f"Text '{key}' updated.")

    def _check_formatting_errors(self, key: str, text: str) -> None:
        """
        Checks for formatting errors in the text (e.g., incorrect curly braces).

        Args:
            key (str): The Redis key of the text.
            text (str): The text content to validate.

        Raises:
            SystemExit: If formatting errors are detected.
        """
        incorrect_patterns = re.findall(r"(?<!{){(?!{)|(?<!})}(?!})", text)
        if incorrect_patterns:
            logger.error(
                f"Formatting error in key '{key}': incorrect curly braces detected. Please fix it."
                )
            sys.exit(
                f"Critical error: Formatting issue in key '{key}'. Script terminated."
                )

    def _log_all_texts(self) -> None:
        """
        Logs all text entries currently loaded in the instance.
        """
        logger.info("Logging all texts from Redis:")
        for key, value in self.texts.items():
            logger.info(f"{key}: {value}")

    def __getattr__(self, name: str) -> "Content":
        """
        Dynamically retrieves a text entry as a Content object.

        Args:
            name (str): The name of the text entry to retrieve.

        Returns:
            Content: A Content object wrapping the text entry.
        """
        redis_key = f"text:{name}"
        text = self.texts.get(redis_key, f"Default {name.replace('_', ' ').title()}")
        return Content(text)


class Content:
    """
    Wrapper class for text content that supports dynamic formatting.
    """

    def __init__(self, message: str):
        """
        Initializes the Content object with a message.

        Args:
            message (str): The text message to wrap.
        """
        self.message = message

    def __call__(self, **kwargs) -> str:
        """
        Formats the text message with the provided keyword arguments.

        Args:
            **kwargs: Key-value pairs to replace placeholders in the text.

        Returns:
            str: The formatted text message.
        """
        result = self.message
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result


bot_content = TextContent()

__all__ = ["bot_content"]
