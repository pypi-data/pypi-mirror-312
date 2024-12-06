from typing import Optional, Dict
from redis.asyncio import Redis
from loguru import logger
import re
import sys


# Синглтон для хранилища текстов с возможностью быстро отправлять их.
# Использование:
# В редис.
# Ключ: text:welcome_message
# Значение: Привет, {{name}}
#
# Использование
# text = text.welcome_message.edit(name="Igor") -> Привет, Igor
# text = text.welcome_message -> Привет, {{name}}


class TextContent:
    _instance: Optional["TextContent"] = None
    texts: Dict[str, str] = {}
    redis: Optional[Redis] = None

    def __new__(cls) -> "TextContent":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, redis_instance: Redis) -> None:
        if not redis_instance:
            raise ValueError("Redis instance is required for initializing TextContent.")
        self.redis = redis_instance
        logger.success("Initializing texts from Redis...")
        await self.update_all()
        self._log_all_texts()

    async def update_all(self) -> None:
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        keys = await self.redis.keys("text:*")
        for key in keys:
            text = await self.redis.get(key)
            self.texts[key] = text
            self._check_formatting_errors(key, text)
        logger.success("All texts updated.")

    async def update(self, key: str) -> None:
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        redis_key = f"text:{key}"
        text = await self.redis.get(redis_key)
        self.texts[redis_key] = text
        self._check_formatting_errors(redis_key, text)
        logger.success(f"Text '{key}' updated.")

    def _check_formatting_errors(self, key: str, text: str) -> None:
        incorrect_patterns = re.findall(r"(?<!{){(?!{)|(?<!})}(?!})", text)
        if incorrect_patterns:
            logger.error(
                f"Formatting error in key '{key}': incorrect curly braces detected. Please fix it."
            )
            sys.exit(
                f"Critical error: Formatting issue in key '{key}'. Script terminated."
            )

    def _log_all_texts(self) -> None:
        logger.info("Logging all texts from Redis:")
        for key, value in self.texts.items():
            logger.info(f"{key}: {value}")

    def __getattr__(self, name: str) -> "Content" or str:
        redis_key = f"text:{name}"
        text = self.texts.get(redis_key, f"Default {name.replace('_', ' ').title()}")
        if "{" in text and "}" in text:  # Если есть форматирование
            return Content(text)
        return text  # Если текст без форматирования, возвращаем строку напрямую


class Content:
    def __init__(self, message: str):
        self.message = message

    def edit(self, **kwargs) -> str:
        result = self.message
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result


bot_content = TextContent()

__all__ = ["bot_content"]
