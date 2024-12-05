from fastapi import FastAPI, APIRouter
from api.teams import team_router
from db.session import metadata, engine
from fastapi.middleware.cors import CORSMiddleware

metadata.create_all(engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def include_router(router: APIRouter):
    app.include_router(router)
