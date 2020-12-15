from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    def create(self, db: Session, obj_in: Union[CreateSchemaType, dict]) -> ModelType:
        """Create a database object.

        Args:
            db (Session): Database session.
            obj_in (Union[CreateSchemaType, dict]): Object data.

        Raises:
            TypeError: Wrong column used on `obj_in`.
            sqlalchemy.exc.DataError: Invalid value on PostgreSQL.
            sqlalchemy.exc.OperationalError: Invalid value on MySQL.

        Returns:
            ModelType: Created object.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get(self, session: Session, *args, **kwargs) -> ModelType:
        """Get a single database object.

        Args:
            session (Session): Database session.

        Returns:
            ModelType: Database object found.
        """
        return session.query(self._model).filter(*args).filter_by(**kwargs).first()

    def get_multi(
        self,
        session: Session,
        *args,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        **kwargs
    ) -> List[ModelType]:
        """Get multiple database objects.

        Args:
            session (Session): Database session.
            offset (Optional[int], optional): [description]. Defaults to None.
            limit (Optional[int], optional): [description]. Defaults to None.
            order_by (Optional[str], optional): [description]. Defaults to None.

        Returns:
            List[ModelType]: Database objects found.
        """
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
        """Count number of objects based on filters `args` and `kwargs`.

        Args:
            session (Session): Database session.

        Returns:
            int: Number of objects found.
        """
        return session.query(self._model).filter(*args).filter_by(**kwargs).count()

    def update(
        self, session: Session, obj_in: Union[UpdateSchemaType, dict], **kwargs
    ) -> ModelType:
        """Update database object based on `obj_update` new values.

        Args:
            session (Session): Database session.
            obj_update (Union[UpdateSchemaType, dict]): New values.

        Returns:
            ModelType: Database object updated.
        """
        db_obj = self.get(session, **kwargs)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        session.commit()
        return db_obj

    def delete(self, session: Session, *args, **kwargs) -> ModelType:
        """Delete database object.

        Args:
            session (Session): Database session.

        Raises:
            NoResultFound: if no row was found.
            MultipleResultsFound: if multiple rows were found.

        Returns:
            ModelType: Deleted database object.
        """
        obj = self.get(session, *args, **kwargs)
        session.delete(obj)
        session.commit()
        return obj
