# /auth-service/app/util/exceptions.py
class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

class UserAlreadyExistsError(ServiceError):
    def __init__(self, message="Email já cadastrado."):
        super().__init__(message, status_code=409)

class AuthenticationError(ServiceError):
    def __init__(self, message="Email ou senha inválidos."):
        super().__init__(message, status_code=401)