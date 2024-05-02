from typing import Optional
from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
import psycopg2
from pydantic import BaseModel
# from .models import User, Post

class User(BaseModel):
    id_user: Optional[int]
    username: str
    password: str
    created_at: date
    updated_at: Optional[date]

class Post(BaseModel):
    id_post: int
    user_id: int
    text: str
    created_at: date
    updated_at: Optional[date]

app = FastAPI()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="socmed",
    user="postgres",
    password="1234QWer",
    # host="*"
    client_encoding='UTF8'
)
cur = conn.cursor()

# API Для регистрации пользователей
@app.post("/registration/")
async def registration(userReg: User):
    query = "INSERT INTO \"User\" (username, password, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id_user"
    cur.execute(query, (userReg.username, userReg.password, userReg.created_at, userReg.updated_at))
    id_user = cur.fetchone()[0]
    conn.commit()
    # return {"id_user": id_user,"username": userReg.username, "created_at": userReg.created_at}
    return {"username": userReg.username, "created_at": userReg.created_at}

# API Для логина пользователей
@app.post("/login/")
async def login(userLog: User):
    query = "SELECT id_user FROM \"User\" WHERE username = %s AND password = %s"
    cur.execute(query, (userLog.username,userLog.password))
    id_usergg = cur.fetchone()[0]
    conn.commit()
    if userLog.id_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return {"message": "User logged in succesfully", "id_user": id_usergg}

# API для публикации новых постов
@app.post("/User/{user_id}/Post/")
async def create_post(user_id: int, postCrt: Post):
    query = "INSERT INTO \"Post\" (user_id, text, created_at) VALUES (%s, %s, %s) RETURNING id_post"
    cur.execute(query, (user_id, postCrt.text, postCrt.created_at))
    id_post = cur.fetchone()[0]
    conn.commit()
    return {"id_post": id_post, "user_id": user_id, "text": postCrt.text, "created_at": postCrt.created_at}

# API для редактирования постов
@app.put("/users/{user_id}/posts/{id_post}/")
async def update_post(postRed: Post):
    query = "UPDATE \"Post\" SET text = %s, updated_at = %s WHERE id_post = %s AND user_id = %s"
    cur.execute(query, (postRed.text, postRed.updated_at, postRed.id_post, postRed.user_id))
    conn.commit()
    return {"id_post": postRed.id_post, "user_id": postRed.user_id, "text": postRed.text, "updated_at": postRed.updated_at}

# API для удаления постов пользователей
@app.delete("/users/{user_id}/posts/{id_post}/")
async def delete_post(user_id: int, id_post: int):
    query = "DELETE FROM \"Post\" WHERE id_post = %s AND user_id = %s"
    cur.execute(query, (id_post, user_id))
    conn.commit()
    return {"message": "Post with id {} has been deleted".format(id_post)}

# API для просмотра постов пользователей по их внутреннему идентификатору
@app.get("/users/{user_id}/posts/")
async def get_user_posts(user_id: int):
    query = "SELECT id_post, user_id, text, created_at, updated_at FROM \"Post\" WHERE user_id = %s"
    cur.execute(query, (user_id,))
    posts = cur.fetchall()
    return posts

