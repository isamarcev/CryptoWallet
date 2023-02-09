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
    rabbit_host: str
    rabbit_port: int
    rabbit_user: str
    rabbit_pass: str
    rabbit_vhost: str
    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    #digital_ocean_space
    space_name: str
    space_access_key: str
    space_secret_key: str
    space_region: str

    #infura ethereum node
    infura_api_url: str
    infura_api_key: str

    #redis url
    redis_url: str
    #etherscan
    # etherscan_get_block_url: str
    # etherscan_api_key: str



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

    @property
    def space_endpoint_url(self) -> URL:
        """
        Assemble DigitalOceanSpace URL from settings.
        Returns: space URL.

        """

        return URL.build(
            scheme='https',
            host=f"{self.space_region}.digitaloceanspaces.com"
        )

    @property
    def space_url(self) -> URL:
        """
        Assemble DigitalOceanSpace URL from settings.
        Returns: space URL.

        """

        return URL.build(
            scheme='https',

            host=f"{self.space_name}.{self.space_region}.digitaloceanspaces.com"
        )

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
