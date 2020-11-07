from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    def create(self, db: Session, obj_in: Union[CreateSchemaType, dict]) -> ModelType:
        """[summary]

        Args:
            db (Session): [description]
            obj_in (Union[CreateSchemaType, dict]): [description]

        Raises:
            TypeError: if wrong column is used on `obj_in`.
            ValidationError: if wrong value on any `obj_in` field.

        Returns:
            ModelType: [description]
        """
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self._model(**obj_in_data)
            db.add(db_obj)
            db.commit()
        except (TypeError, ValidationError) as exc:
            raise exc
        else:
            return db_obj

    def get(self, session: Session, *args, **kwargs) -> ModelType:
        """[summary]

        Args:
            session (Session): [description]

        Raises:
            NoResultFound: if no row was found.
            MultipleResultsFound: if multiple rows were found.

        Returns:
            ModelType: [description]
        """
        # for arg in args:
        #     print(type(arg))
        # print(type(args))
        try:
            query = session.query(self._model).filter(*args).filter_by(**kwargs).one()
        except (NoResultFound, MultipleResultsFound) as exc:
            raise exc
        else:
            return query

    def get_multi(
        self,
        session: Session,
        *args,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        **kwargs
    ) -> List[ModelType]:
        return (
            session.query(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count(self, session: Session, *args, **kwargs) -> int:
        return session.query(self._model).filter(*args).filter_by(**kwargs).count()

    # TODO: Should args be added?
    def update(
        self,
        session: Session,
        obj_update: Union[UpdateSchemaType, Dict[str, Any]],
        *args,
        **kwargs
    ) -> ModelType:
        if isinstance(obj_update, dict):
            data = obj_update
        else:
            data = obj_update.dict(exclude_unset=True)
        obj = session.query(self._model).filter(*args).filter_by(**kwargs).update(data)
        session.commit()
        return obj

    def delete(self, session: Session, *args, **kwargs) -> ModelType:
        obj = self.get(session, *args, **kwargs)
        session.delete(obj)
        session.commit()
        return obj
