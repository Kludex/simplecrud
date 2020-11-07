from ._sqlalchemy import CRUDBase


class CRUDFactory:
    @staticmethod
    def get_sqlalchemy(model_type, create_schema, update_schema):
        return CRUDBase[model_type, create_schema, update_schema](model_type)


# TODO: Create a support for own factories and CRUD classes.
