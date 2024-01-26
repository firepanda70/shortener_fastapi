from pathlib import Path

from fastapi.testclient import TestClient

import pytest_asyncio
import pytest
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine

from scr.core.base import BaseDBModel
from scr.core.db import get_async_session
from app import app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite://{str(TEST_DB)}'

pytest_plugins = [
    'tests.fixtures.data',
]

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)

@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)

async def override_get_async_session():
    async with TestingSessionLocal() as async_session:
        yield async_session

app.dependency_overrides[get_async_session] = override_get_async_session

test_client = TestClient(app)

@pytest.fixture
def mixer():
    mixer_engine = create_engine(f'sqlite://{str(TEST_DB)}')
    session = sessionmaker(bind=mixer_engine)
    return _mixer(session=session(), commit=True)
