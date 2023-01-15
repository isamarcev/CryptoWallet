
class JWTBackend:

    def __init__(self, jwt_secret_key, jwt_algorithm, jwt_expire):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expire = jwt_expire