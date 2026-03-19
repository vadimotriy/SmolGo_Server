from fastapi import FastAPI
from app.models import *
from databases import Database
from contextlib import asynccontextmanager
import hashlib
import datetime
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

app = FastAPI(lifespan=lifespan)

@app.post("/registration")
async def create_item(data: Registration):
    query = """
        SELECT id
        FROM users
        WHERE email = :user_email
    """

    try:
        result = await database.fetch_one(
            query=query,
            values={"user_email": data.email}
        )

    except Exception:
        return {"message": "Fail"}
    
    if result is None:
        query1 = """
            INSERT INTO users (email, password)
            VALUES (:email, :password)
            RETURNING id
        """

        query2 = """
            INSERT INTO users_information (name, registration)
            VALUES (:name, :registration)
        """

        text = data.password.encode("utf-8")
        text = hashlib.sha256(text).hexdigest()

        user_id = await database.execute(
            query=query1,
            values={"email": data.email, "password": text}
        )

        await database.execute(
            query=query2,
            values={"name": data.name, "registration": str(datetime.date.today())}
        )

        return {"message": "Succes"}
    return {"message": "Email is used"}


@app.post("/login")
async def login(data: Login):
    query = """
        SELECT id
        FROM users
        WHERE email = :user_email
    """

    try:
        result = await database.fetch_one(
            query=query,
            values={"user_email": data.email}
        )

    except Exception:
        return {"message": "Fail"}
    
    if result is not None:
        result = dict(result)
        id = result["id"]

        query = """
            SELECT name
            FROM users_information
            WHERE id = :user_id
        """

        result = await database.fetch_one(
            query=query,
            values={"user_id": id}
        )
        result = dict(result)

        text = data.password.encode("utf-8")
        text = hashlib.sha256(text).hexdigest()

        return {"message": "Succes",
                "name": result["name"]}
    
    return {"message": "Email has not been used"}