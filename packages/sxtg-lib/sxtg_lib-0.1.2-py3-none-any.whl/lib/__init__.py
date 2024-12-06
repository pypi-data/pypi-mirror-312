from .__main__ import redis, bot_content, bot_settings


async def start_sxtg(REDIS_URL: str):
    try:
        await redis.initialize(REDIS_URL)
        await bot_settings.initialize(redis.connection)
        await bot_content.initialize(redis.connection)
        if bot_settings.echo is True:
            print("Echo включено")
        elif bot_settings.echo is False:
            print("Echo выключено")
        elif bot_settings.echo == "44":
            print("Echo 44")
        print(bot_content.meme)
    except Exception as e:
        print(f"Failed to initialize Redis or BotSettings: {e}")
    finally:
        await redis.close()
