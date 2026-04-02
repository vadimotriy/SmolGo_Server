from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Registration(BaseModel):
    name: str
    email: str
    password: str


class News(BaseModel):
    password: str
    link: str
    title: str
    text: str
    date: str
