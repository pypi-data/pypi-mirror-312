
# Async SQL Server Library

A lightweight Python library for managing asynchronous connections to SQL Server databases, designed for modern Python applications requiring robust, reusable, and efficient database management.

This library simplifies SQL Server database interactions using SQLAlchemy's async capabilities and aioodbc. It provides decorators for managing connections, commits, and rollbacks, ensuring clean and consistent database handling across your projects.

---

## Installation

### Using Pip
To install the library, run:
```bash
pip install async-sqlserver-lib
```

### Using Pipenv
If you're using pipenv for dependency management:
```bash
pipenv install async-sqlserver-lib
```

---

## Purpose

### Why Use This Library?
1. **Asynchronous Database Operations**: Ideal for APIs and high-performance Python applications.
2. **Simplified Connection Management**: Provides reusable decorators for creating and closing database connections.
3. **SQLAlchemy and aioodbc Integration**: Leverages SQLAlchemy for ORM and query execution, and aioodbc for async database communication.
4. **Ease of Use**: Write clean, readable, and maintainable database interaction code with minimal setup.

---

## Running Tests

### Prerequisites
Install testing dependencies:
```bash
pip install pytest pytest-asyncio
```

### Run the Test Suite
Execute all tests with:
```bash
pytest
```

The test suite validates:
1. Connection management.
2. Decorator functionality.
3. Query execution.

---


## Contact and Support

For questions, issues, or contributions, please open an issue or pull request in the [GitHub repository](https://github.com/brandaolu94s/async-sqlserver-lib).

---

## Acknowledgments

This library builds upon the powerful features of:
- [SQLAlchemy](https://www.sqlalchemy.org/) for its async database management capabilities.
- [aioodbc](https://github.com/aio-libs/aioodbc) for asynchronous ODBC driver integration.
