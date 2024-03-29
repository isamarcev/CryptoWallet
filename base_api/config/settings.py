# -*- coding: utf-8 -*-
from pathlib import Path

from pydantic import BaseSettings
from yarl import URL

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):

    backend_url: str
    asyncapi_docs_url: str

    test_postgres_host: str = "localhost"
    test_postgres_port: int = 5432
    test_postgres_user: str
    test_postgres_password: str
    test_postgres_db: str
    test_postgres_echo: bool = False


    # postgres_db
    postgres_pass: str
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_user: str
    postgres_name: str

    # jwt settings
    jwt_secret_key: str
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
    etherscan_key: str

    # owner_wallet
    owner_public_key: str

    #email
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str


    #sqlalchemy_admin
    sqlalchemy_secret_key: str

    #user_data_for_testing
    user_email: str
    username: str
    password: str

    @property
    def test_db_url(self) -> URL:
        """
        Assemble database URL from settings.
        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.test_postgres_host,
            port=self.test_postgres_port,
            user=self.test_postgres_user,
            password=self.test_postgres_password,
            path=f"/{self.test_postgres_db}",
        )


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
        env_file = BASE_DIR / ".env.prod"


settings = Settings()
