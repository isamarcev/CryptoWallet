from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta

from base_api.config.settings import settings


class JWTBackend:

    def __init__(self, jwt_secret_key, jwt_algorithm, jwt_expire):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expire = jwt_expire

    async def create_access_token(self, payload: Dict) -> tuple:
        expiration = datetime.utcnow() + timedelta(days=self.jwt_expire)
        payload.update({"exp": expiration})
        access_token = jwt.encode(payload,
                                  self.jwt_secret_key,
                                  self.jwt_algorithm)
        return {"username": payload.get("username"),
                'expiration': payload.get("exp")}, access_token

    @staticmethod
    async def decode_token(token: str) -> Optional[Dict]:
        if token:
            try:
                decoded_token = jwt.decode(token,
                                           settings.jwt_secret_key,
                                           settings.jwt_algorithm)
                return decoded_token
            except Exception:
                return None
        return None
