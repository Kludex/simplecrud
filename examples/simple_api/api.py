from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from examples.simple_api.crud import crud_user
from examples.simple_api.database import get_session
from examples.simple_api.schemas import UserCreate, UserInDB, UserOut, UserUpdate
from examples.simple_api.utils import fake_hash

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_model=List[UserOut])
def get_users(session: Session = Depends(get_session)):
    return crud_user.get_multi(session)


@router.get(
    "/{user_id}",
    responses={"404": {"description": "User not found."}},
    response_model=UserOut,
)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.post(
    "/",
    status_code=201,
    responses={"409": {"description": "User already exists."}},
    response_model=UserOut,
)
def post_user(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        user = crud_user.create(
            session,
            UserInDB(**user_in.dict(), password_hash=fake_hash(user_in.password)),
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists.")
    return user


@router.put(
    "/{user_id}",
    responses={
        "404": {"description": "User not found."},
        "409": {"description": "User already exists."},
    },
    response_model=UserOut,
)
def put_user(
    user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)
):
    try:
        user = crud_user.update(session, user_in, id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists.")
    return user


@router.delete(
    "/{user_id}", status_code=204, responses={"404": {"description": "User not found."}}
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = crud_user.delete(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
