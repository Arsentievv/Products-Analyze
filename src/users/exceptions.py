class UserNotFoundError(Exception):
    detail = "User Not Found"


class IncorrectPasswordError(Exception):
    detail = "Inserted Password Is Incorrect"
