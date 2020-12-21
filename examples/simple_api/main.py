from fastapi import FastAPI

from examples.simple_api.api import router as user
from examples.simple_api.database import Base, engine

app = FastAPI()
app.include_router(user, prefix="/v1")

Base.metadata.create_all(bind=engine)
