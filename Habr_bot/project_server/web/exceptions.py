class Error(Exception):
    status: int = 500
    code: str = "internal_error"
    description: str = "Internal Error"


class AlreadyExists(Error):
    status = 400
    code = "already_exists"
    description = "User already exists"


class InvalidCredentials(Error):
    status = 400
    code = "invalid_credentials"
    description = "Username or password incorrect"


class NotFound(Error):
    status = 404
    code = "not found"
    description = "Entity not found"


class NotAuthorized(Error):
    status = 401
    code = "not_authorized"
    description = "Not Authorized"
