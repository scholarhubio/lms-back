from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import postgres, redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis
from core import settings


@asynccontextmanager
async def setup_lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port, decode_responses=True)
    postgres.async_engine = create_async_engine(
        settings.postgres.adsn,
        pool_pre_ping=True, pool_size=20, pool_timeout=30)
    postgres.async_session_factory = sessionmaker(
        postgres.async_engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession)
    yield
    await postgres.async_engine.dispose()
    postgres.async_session_factory.close_all()
    await redis.redis.close()
