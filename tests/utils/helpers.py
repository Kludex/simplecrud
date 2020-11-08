from sqlalchemy.orm import Session

from crudfactory.factories import CRUDFactory
from tests.utils.models import User
from tests.utils.schemas import UserCreate, UserUpdate

crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
