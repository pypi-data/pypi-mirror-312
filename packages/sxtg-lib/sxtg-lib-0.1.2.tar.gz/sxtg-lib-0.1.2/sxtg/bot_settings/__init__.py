from typing import Optional, Dict, Union
from redis.asyncio import Redis
from loguru import logger

class BotSettings:
    _instance: Optional["BotSettings"] = None
    settings: Dict[str, Union[bool, str]] = {}
    redis: Optional[Redis] = None

    def __new__(cls) -> "BotSettings":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, redis_instance : Redis) -> None:
        if not redis_instance:
            raise ValueError("Redis instance is required for initialization bot setting")
        self.redis = redis_instance
        logger.success("Initializing bot settings from Redis...")
        await self.update_all()
        self._log_all_settings()
        logger.info(f"Current settings: {self.settings}")

    async def update_all(self) -> None:
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        keys = await self.redis.keys("bot_setting:*")
        for key in keys:
            value = await self.redis.get(key)
            self._set_setting(key, value)
        logger.success("All settings updated.")

    async def update(self, key: str) -> None:
        if not self.redis:
            raise RuntimeError("Redis instance is not initialized.")
        redis_key = f"bot_setting:{key}"
        value = await self.redis.get(redis_key)
        self._set_setting(redis_key, value)
        logger.success(f"Setting '{key}' updated.")

    def _set_setting(self, key: str, value: str) -> None:
        if value == "0":
            self.settings[key] = False
        elif value == "1":
            self.settings[key] = True
        else:
            self.settings[key] = value

    def _log_all_settings(self) -> None:
        logger.info("Logging all:")
        for key, value in self.settings.items():
            logger.info(f"{key}: {value}")

    def __getattr__(self, name: str) -> Union[bool, str]:
        redis_key = f"bot_setting:{name}"
        return self.settings.get(redis_key, False)


bot_settings = BotSettings()

__all__ = ["bot_settings"]