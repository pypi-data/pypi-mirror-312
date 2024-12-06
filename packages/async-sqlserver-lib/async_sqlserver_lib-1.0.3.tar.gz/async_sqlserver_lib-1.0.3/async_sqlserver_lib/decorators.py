from functools import wraps
from typing import Callable, Any
from .db_manager import DBManager

def create_db_connection(driver: str, user: str, password: str, host: str, port: int, database: str) -> Callable:
    """
    Decorator to initialize a database connection.

    :param driver: ODBC driver for SQL Server.
    :param user: Username for the database.
    :param password: Password for the database.
    :param host: Host address of the database.
    :param port: Port number of the database.
    :param database: Name of the database.
    :return: A decorator for injecting a DBManager instance.
    """
    db_manager = DBManager(driver, user, password, host, port, database)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            kwargs["db_manager"] = db_manager  # Inject DBManager into the function.
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def close_db_connection(func: Callable) -> Callable:
    """
    Decorator to ensure the database connection is closed after use.

    :param func: The async function to wrap.
    :return: A wrapped function that ensures the DB engine is closed.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        db_manager: DBManager = kwargs.get("db_manager")
        try:
            result = await func(*args, **kwargs)  # Call the decorated function.
            return result
        finally:
            if db_manager:
                await db_manager.close_engine()  # Close the DB engine.

    return wrapper
