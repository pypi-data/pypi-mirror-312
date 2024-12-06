from setuptools import setup, find_packages

setup(
    name="async-sqlserver-lib",  
    version="1.0.3",  
    description="A Python library for managing asynchronous SQL Server connections.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown", 
    author="Lucas Brandão",
    author_email="lbsantos@bencorp.com.br", 
    url="https://github.com/brandaolu94s/async-sqlserver-lib",
    packages=find_packages(),  
    install_requires=[
        "setuptools",  # Required for the package to work
        "wheel",  # Helps build wheel distributions
        "sqlalchemy[asyncio]>=1.4",  # SQLAlchemy with asyncio support
        "aioodbc>=0.2.6",  # Async ODBC driver
        "python-dotenv>=0.21.0",  # For .env management
    ],
    extras_require={
        "dev": [
            "pytest",  # For testing
            "pytest-asyncio",  # For async test support
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Enforce Python 3.8+
    license="MIT",  # License type
    keywords="sql-server asyncio sqlalchemy aioodbc",
)