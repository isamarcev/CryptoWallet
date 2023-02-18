from functools import lru_cache
from pathlib import Path

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

from base_api.config.settings import settings


class EmailClient:
    def __init__(self, username: str, password: str, mail_from: str, mail_port: int, server: str,):
        self.conf = ConnectionConfig(
            MAIL_SERVER=server,
            MAIL_PORT=mail_port,
            MAIL_USERNAME=username,
            MAIL_PASSWORD=password,
            MAIL_FROM=mail_from,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / "templates/emails"
        )

    async def send_email_new_user(self, body: dict):
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=[body['email']],
            template_body={"username": body['user']},
            subtype=MessageType.html,
        )

        fm = FastMail(self.conf)
        await fm.send_message(message, template_name='new_user.html')


@lru_cache()
def new_email_client() -> EmailClient:
    return EmailClient(
        username=settings.mail_username,
        password=settings.mail_password,
        mail_from=settings.mail_from,
        mail_port=settings.mail_port,
        server=settings.mail_server
    )
