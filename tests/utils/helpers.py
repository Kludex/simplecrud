from simplecrud.sync_sqlalchemy import CRUDBase
from tests.utils.models import User
from tests.utils.schemas import UserCreate, UserUpdate

crud_user = CRUDBase[User, UserCreate, UserUpdate](User)
