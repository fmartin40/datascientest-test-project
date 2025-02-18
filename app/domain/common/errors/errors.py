
class Error(Exception):
    errno: int | None
    message: str | None

class NotFoundException(Error):
    pass

class FetchApiException(Error):
    pass

class RepositoryError(Error):
    pass

class AlreadyExistError(Error):
    pass

# utilisée par la classe Entity
# indique les valeurs manquantes lors de la creation d'une entité
class MissingValueException(Exception):
    def __init__(
        self,
        entity: str,
        message: str
        # status: StatusType = StatusType.PARAMETERS_ERROR,
    ) -> None:
        self.entity = entity
        self.message = message
        

    def __str__(self) -> str:
        return f"Il manque un attribut dans {self.entity} --> {self.message}"
