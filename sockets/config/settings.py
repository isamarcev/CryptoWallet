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

    # rabbitmq
    rabbit_host: str = "rabbitmq"
    rabbit_port: int = 15672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    # mongodb
    # mongo_host: str = "localhost"
    # mongo_port: str
    # mongo_name: str

    @property
    def postgres_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.

        """
        return URL.build(
            scheme="postgresql",
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

    # @property
    # def mongodb_url(self) -> URL:
    #     """
    #     Assemble MongoDB URL from settings.
    #
    #     :return: mongodb URL.
    #
    #     """
    #     return URL.build(
    #         scheme="mongodb",
    #         host=self.mongo_host,
    #         port=self.mongo_port,
    #     )

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
