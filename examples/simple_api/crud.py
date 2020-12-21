from simplecrud.sync_sqlalchemy import CRUDBase

from examples.simple_api.models import User
from examples.simple_api.schemas import UserInDB, UserUpdate

crud_user = CRUDBase[User, UserInDB, UserUpdate](User)
