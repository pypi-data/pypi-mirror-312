import urllib.parse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

class DBManager:
    """
    Manages asynchronous database connections for SQL Server using SQLAlchemy.
    """

    def __init__(
        self,
        driver: str,
        user: str,
        password: str,
        host: str,
        port: int,
        database: str,
    ) -> None:
        """
        Initializes the DBManager with connection parameters.

        :param driver: ODBC driver for SQL Server (e.g., "ODBC Driver 17 for SQL Server").
        :param user: Username for the database.
        :param password: Password for the database.
        :param host: Host address of the database.
        :param port: Port number of the database.
        :param database: Name of the database.
        :raises ValueError: If any connection parameter is invalid.
        """
        # Validate input parameters
        self._validate_params(driver, user, password, host, port, database)

        try:
            self.connection_string = self._format_connection_string(
                driver, user, password, host, port, database
            )
            self.engine = create_async_engine(
                self.connection_string, echo=False, future=True
            )
            self.Session = sessionmaker(
                bind=self.engine, class_=AsyncSession, expire_on_commit=False
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DBManager: {str(e)}")

    def _validate_params(
        self,
        driver: Optional[str],
        user: Optional[str],
        password: Optional[str],
        host: Optional[str],
        port: Optional[int],
        database: Optional[str],
    ) -> None:
        """
        Validates connection parameters.

        :param driver: ODBC driver for SQL Server.
        :param user: Username for the database.
        :param password: Password for the database.
        :param host: Host address of the database.
        :param port: Port number of the database.
        :param database: Name of the database.
        :raises ValueError: If any parameter is missing or invalid.
        """
        if not driver:
            raise ValueError("Database driver is required.")
        if not user:
            raise ValueError("Database user is required.")
        if not password:
            raise ValueError("Database password is required.")
        if not host:
            raise ValueError("Database host is required.")
        if not isinstance(port, int) or port <= 0:
            raise ValueError("Database port must be a positive integer.")
        if not database:
            raise ValueError("Database name is required.")

    def _format_connection_string(
        self, driver: str, user: str, password: str, host: str, port: int, database: str
    ) -> str:
        """
        Formats the connection string for SQL Server.

        :param driver: ODBC driver for SQL Server.
        :param user: Username for the database.
        :param password: Password for the database.
        :param host: Host address of the database.
        :param port: Port number of the database.
        :param database: Name of the database.
        :return: A formatted connection string.
        """
        from urllib.parse import quote_plus

        return f"mssql+aioodbc:///?odbc_connect={quote_plus(f'DRIVER={driver};SERVER={host};PORT={port};DATABASE={database};UID={user};PWD={password}')}"

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides a database session as a context manager.

        :yield: An AsyncSession instance.
        """
        session = self.Session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close_engine(self) -> None:
        """
        Closes the database engine and releases resources.

        :return: None
        """
        try:
            # Dispose the engine to release resources
            await self.engine.dispose()

            # Optionally set the engine to None to prevent reuse
            self.engine = None
        except Exception as e:
            raise RuntimeError(f"Failed to close engine: {str(e)}")

        # Explicitly return None for clarity
        return self.engine
