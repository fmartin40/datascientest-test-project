
# class FetchApiException(Exception):
#     def __init__(self, status_code: int, message: str):
#         self.status_code = status_code
#         self.message = message
#         super().__init__(f"Status Code: {status_code}, Message: {message}")

class Error(Exception):
    errno: int | None
    message: str | None

class FetchApiException(Error):
    pass

class RepositoryError(Error):
    pass


class AlreadyExistError(Error):
    pass