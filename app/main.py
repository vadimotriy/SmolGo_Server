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
        return {"message": "Fail on DB"}
    
    if result is not None:
        result = dict(result)
        id = result["id"]

        query1 = """
            SELECT name
            FROM users_information
            WHERE id = :user_id
        """

        query2 = """
            SELECT password
            FROM users
            WHERE id = :user_id
        """

        result = await database.fetch_one(
            query=query1,
            values={"user_id": id}
        )
        result = dict(result)

        password = await database.fetch_one(
            query=query2,
            values={"user_id": id}
        )
        password = dict(password)

        text = data.password.encode("utf-8")
        text = hashlib.sha256(text).hexdigest()

        if text != password["password"]:
            return {"message": "Password is not correct"}

        return {"message": "Succes",
                "name": result["name"]}
    
    return {"message": "Email has not been used"}


@app.post("/create_news")
async def create_news(data: News):
    if data.password != "FHA)*SYD97SYG(!G@!GJGDAS9yu)werh*YWdq1j;!01":
        return {"message": "Password is not correct"}

    query = """
        INSERT INTO news (link, title, text, date)
        VALUES (:link, :title, :text, :date)
    """
    try:
        await database.execute(
            query=query,
            values={"link": data.link, "title": data.title, "text": data.text, "date": data.date}
        )
        return {"message": "Succes"}
    except Exception:
        return {"message": "Fail on DB"}


@app.get("/get_news")
async def get_news():
    query = """
        SELECT *
        FROM news
        ORDER BY id
        DESC LIMIT 3;
    """

    try:
        result = await database.fetch_all(
            query=query
        )
        result = [dict(row) for row in result]

        return { "message": "Succes",
                "news_1": result[0],
                "news_2": result[1],
                "news_3": result[2] }
    except Exception:
        return {"message": "Fail on DB"}