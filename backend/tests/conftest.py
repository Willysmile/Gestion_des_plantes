"""
Pytest configuration and fixtures
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import Client

from app.main import app
from app.utils.db import get_db
from app.models.base import BaseModel


# Create test database
TEST_DATABASE_URL = "sqlite:////tmp/test_plants.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create fresh test database for each test"""
    # Create tables
    BaseModel.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    # Drop tables after test
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create FastAPI test client with dependency override"""
    # Override get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test database
    BaseModel.metadata.create_all(bind=engine)
    
    # Create test client using httpx.Client directly
    test_client = Client(app=app, base_url="http://test")
    
    yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    BaseModel.metadata.drop_all(bind=engine)


