from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.src.sql.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
    # '*'
]

from apps.src.routes.apis.v1.user import routes as user_routes
from apps.src.routes.apis.v1.lecture import routes as lecture_routes
from apps.src.routes.apis.v1.data import routes as data_routes

app.include_router(user_routes.rt)
app.include_router(lecture_routes.rt)
app.include_router(data_routes.rt)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
