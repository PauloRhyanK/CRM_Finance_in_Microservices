# /interaction-service/app/util/exceptions.py
class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

class CustomerNotFoundError(ServiceError):
    def __init__(self, message="Cliente não encontrado."):
        super().__init__(message, status_code=404)

class UserNotFoundError(ServiceError):
    def __init__(self, message="Usuário não encontrado."):
        super().__init__(message, status_code=404)

class InvalidDataError(ServiceError):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)