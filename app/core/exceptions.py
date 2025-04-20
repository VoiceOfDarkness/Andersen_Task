from uuid import UUID


class RepositoryException(Exception):
    pass


class ObjectNotFoundException(RepositoryException):
    def __init__(self, model_name: str, obj_id: UUID):
        self.model_name = model_name
        self.obj_id = obj_id
        super().__init__(f"{model_name} with id {obj_id} not found")
