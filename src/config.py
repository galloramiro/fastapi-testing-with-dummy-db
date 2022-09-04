import logging
import os
from pathlib import Path


DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_HOST = os.getenv("DATABASE_HOST", "mysql")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "3306"))
DATABASE_NAME = os.getenv("DATABASE_NAME", "dummy-db")

TEST_DATABASE_HOST = os.getenv("DATABASE_HOST", "mysql-test")
TEST_DATABASE_NAME = os.getenv("DATABASE_NAME", "dummy-db-test")
