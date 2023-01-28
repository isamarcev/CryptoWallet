# -*- coding: utf-8 -*-
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, SecretStr
from yarl import URL

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # postgres_db
    postgres_pass: str
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_user: str
    postgres_name: str

    # jwt settings
    jwt_secret_key: str = "09d25e094faa6ca25563f7099f6f0f4caa6cf63b88e8d3e7"
    jwt_algorithm: str = "HS256"
    jwt_expire: int = 30

    # rabbitmq
    rabbit_host: str = "rabbitmq"
    rabbit_port: int = 15672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    @property
    def postgres_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.

        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_pass,
            path=f"/{self.postgres_name}",
        )

    @property
    def rabbit_url(self) -> URL:
        """
        Assemble RabbitMQ URL from settings.

        :return: rabbit URL.

        """
        return URL.build(
            scheme="amqp",
            host=self.rabbit_host,
            port=self.rabbit_port,
            user=self.rabbit_user,
            password=self.rabbit_pass,
            path=self.rabbit_vhost,
        )

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
