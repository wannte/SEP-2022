from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.src.sql.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

from apps.src.routes.apis.v1.user import routes as user_routes
from apps.src.routes.apis.v1.lecture import routes as lecture_routes
from apps.src.routes.apis.v1.data import routes as data_routes

app.include_router(user_routes.rt)
app.include_router(lecture_routes.rt)
app.include_router(data_routes.rt)