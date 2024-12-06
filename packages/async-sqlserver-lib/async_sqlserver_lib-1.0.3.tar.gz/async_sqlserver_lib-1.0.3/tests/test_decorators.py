import pytest
from async_sqlserver_lib.decorators import create_db_connection, close_db_connection
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
load_dotenv()

# Mock SQL Server database details
DB_CONFIG = {
    "driver": os.getenv('DB_DRIVER'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASS'),
    "host": os.getenv('DB_HOST'),
    "port": int(os.getenv('DB_PORT')),
    "database": os.getenv('DB_NAME'),
}

@create_db_connection(
    driver=DB_CONFIG["driver"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"],
)
@close_db_connection
async def sample_function(db_manager=None):
    """
    Sample function to test decorators.
    """
    async with db_manager.get_session() as session:
        assert isinstance(session, AsyncSession)
        return True

@pytest.mark.asyncio
async def test_decorator_functionality():
    """
    Test if decorators inject DBManager and close the engine properly.
    """
    result = await sample_function()
    assert result is True
