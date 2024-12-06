from .__main__ import redis, bot_content, bot_settings


async def inits(REDIS_URL: str):
    await redis.initialize(REDIS_URL)
    await bot_settings.initialize(redis.connection)
    await bot_content.initialize(redis.connection)


async def close():
    await redis.close()
