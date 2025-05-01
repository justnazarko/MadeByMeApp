"""Environment variables config"""

import json
from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


class EnvVariableNotFound(Exception):
    """Environment variable not found"""


@dataclass
class DatabaseConfig:
    """Database config args"""

    user: str = None
    password: str = None
    host: str = None
    port: int = None
    name: str = None


class DbConfig:
    """Database config"""

    def __init__(self, db_config: DatabaseConfig):
        self.user = db_config.user
        self.password = db_config.password
        self.host = db_config.host
        self.port = db_config.port
        self.name = db_config.name
        self.url = (
            f"postgresql+asyncpg://{db_config.user}:"
            f"{db_config.password}@{db_config.host}:"
            f"{db_config.port}/{db_config.name}"
        )


@dataclass
class BackendConfig:
    """Backend config"""

    host: str = None
    port: int = None
    secret_key: str = None
    web_domain: str = None
    logging_level: str = None


class Config:
    """Environment variables config"""

    def __init__(self):
        load_dotenv()
        self.db = DbConfig(
            db_config=DatabaseConfig(
                user=self.get_var("DB_USER"),
                password=self.get_var("DB_PASSWORD"),
                host=self.get_var("DB_HOST"),
                port=int(self.get_var("DB_PORT")),
                name=self.get_var("DB_NAME"),
            )
        )

        self.backend = BackendConfig(
            host=getenv("HOST") if getenv("HOST") else "0.0.0.0",
            port=int(getenv("PORT")) if getenv("PORT") else 8080,
            secret_key=self.get_var("SECRET_KEY"),
            web_domain=self.get_var("WEB_DOMAIN"),
            logging_level=(
                getenv("LOGGING_LEVEL") if getenv("LOGGING_LEVEL") else "INFO"
            ),
        )


    @staticmethod
    def get_var(item: str):
        """Returns environment variable"""
        var = getenv(item)
        if not var:
            raise EnvVariableNotFound(f"Environment variable {item} not found")
        return var


config = Config()
