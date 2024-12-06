import pytest
from async_sqlserver_lib.db_manager import DBManager
from dotenv import load_dotenv
import os

load_dotenv()

# Mock SQL Server database details for testing
DB_CONFIG = {
    "driver": os.getenv('DB_DRIVER'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASS'),
    "host": os.getenv('DB_HOST'),
    "port": int(os.getenv('DB_PORT')),
    "database": os.getenv('DB_NAME'),
}

@pytest.mark.asyncio
async def test_db_connection_failure():
    """
    Test if DBManager handles connection errors gracefully.
    """
    with pytest.raises(ValueError, match="Database password is required."):
        # Attempt to create DBManager with missing password
        DBManager(
            driver=DB_CONFIG["driver"],
            user=DB_CONFIG["user"],
            password='',  # Invalid parameter
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
        )


@pytest.mark.asyncio
async def test_db_session_creation():
    """
    Test if DBManager creates a valid session.
    """
    # Correct credentials for the test environment
    db_manager = DBManager(
        driver=DB_CONFIG["driver"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
    )
    async with db_manager.get_session() as session:
        assert session is not None

@pytest.mark.asyncio
async def test_db_engine_closure():
    """
    Test if DBManager closes the engine properly.
    """
    db_manager = DBManager(
        driver=DB_CONFIG["driver"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
    )
    await db_manager.close_engine()
    assert db_manager.engine is None
