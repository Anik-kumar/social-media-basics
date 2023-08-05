import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends

from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routes import posts, users




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="a1s2d3f4;", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)


app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}





