from fastapi import FastAPI, status, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import database
from app.models import PostRequest


# инициализация приложения с базой данных
app = FastAPI(lifespan=database.lifespan)


# общий обработчик исключения валидации длинной ссылки
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/posts/")
@app.get("/posts")
@app.get("/")
async def get_all_posts():
    posts = await database.get_all_posts_from_db()
    context = []
    for post in posts:
         context.append(post.to_dict())
    return JSONResponse(content=context, status_code=status.HTTP_200_OK)


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = await database.get_post_from_db(post_id)
    if post:
        return JSONResponse(content=post.to_dict(), status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = await database.delete_post_from_db(post_id)
    if post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/posts")
async def create_post(data: PostRequest):
    await database.create_post_on_db(data)
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, data: PostRequest):
    post = await database.update_post_on_db(post_id, data)
    if post:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
