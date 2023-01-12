from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, SecretStr

from yarl import URL

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    #postgres_db
    postgres_pass: str = 'admin'
    postgres_host: str = 'localhost'
    postgres_port: str = '5432'
    postgres_user: str = 'nikitin'
    postgres_name: str = 'crypto_wallet_base'

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

    class Config:
        env_file = BASE_DIR / ".env"

    loc = Config().env_file


settings = Settings()
