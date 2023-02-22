# -*- coding: utf-8 -*-
from pathlib import Path

from pydantic import BaseSettings
from yarl import URL

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # rabbitmq
    rabbit_host: str = "rabbitmq"
    rabbit_port: int = 15672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    # redis url
    redis_url: str


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
        env_file = BASE_DIR / ".env.prod"


settings = Settings()
