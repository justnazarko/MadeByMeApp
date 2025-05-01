import logging
import random
from time import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from API.app import models
from API.app.models.posts import Post, HandicraftCategory, PostStatus, Review
from API.app.models.users import User, Favorite
from API.core.database.base import Base
from API.core.database.session import engine, get_session, Session
from API.core.exceptions.base import CustomException


def init_routers(app_: FastAPI) -> None:
    """Initialize routers."""
    #app_.include_router(router, prefix="/api")


def init_listeners(app_: FastAPI) -> None:
    """Initialize listeners."""

    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        request_url = str(request.url)
        client_host = request.client.host
        method = request.method
        headers = dict(request.headers)
        logging.error(
            "Exception occurred! Request info: %s %s from %s. Headers: %s. "
            "Error details: Code: %s, Error code: %s, Message: %s",
            method,
            request_url,
            client_host,
            headers,
            exc.code,
            exc.error_code,
            exc.message,
        )
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_middlewares(app_: FastAPI) -> None:
    """Initialize middlewares."""

    @app_.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time()
        client_host = request.client.host

        # Отримання методу, шляхів, заголовків і тіла запиту
        logging.log(
            20,
            "Request host: %s Request method: %s Request URL: %s Request headers: %s",
            client_host,
            request.method,
            request.url,
            request.headers,
        )
        try:
            response = await call_next(request)
            process_time = time() - start_time
            response.headers["X-Process-Time"] = str(process_time)

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            logging.log(
                20,
                "Response receiver: %s Response status_code: %s Request URL: %s "
                "Response headers: %s Response body: %s",
                client_host,
                response.status_code,
                request.url,
                response.raw_headers,
                response_body.decode("utf-8"),
            )
            process_time = time() - start_time
            new_response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
            new_response.headers["X-Process-Time"] = str(process_time)

            return new_response
        except Exception as exc:  # pylint: disable=W0718
            logging.exception("An exception occurred")
            logging.log(20, "Fatal error")
            process_time = time() - start_time
            return JSONResponse(
                status_code=500,
                content={"message": f"{exc.args}"},
                headers={"X-Process-Time": str(process_time)},
            )


def create_app() -> FastAPI:
    """Create FastAPI app."""
    app_ = FastAPI(openapi_url="/docs/openapi.json")
    init_routers(app_)
    init_listeners(app_)
    init_middlewares(app_)
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    return app_


app = create_app()

async def create_test_data():
    async with Session() as session:
        # Створюємо 10 юзерів
        users = []
        for i in range(10):
            user = User(
                google_id=f"google_{i}",
                phone_number=f"+3805012345{i:02d}",
                email=f"user{i}@example.com",
                name=f"User {i}",
                avatar_url=f"https://example.com/avatar{i}.png"
            )
            session.add(user)
            users.append(user)

        await session.flush()

        # Створюємо 30 постів
        posts = []
        for i in range(30):
            user = random.choice(users)
            post = Post(
                user_id=user.id,
                title=f"Пост {i} від {user.name}",
                content="Опис виробу ручної роботи",
                image_url=f"https://example.com/post{i}.jpg",
                categories=[
                    random.choice(list(HandicraftCategory)).name,  # <- тут .name дає 'CANDLE_MAKING'
                    random.choice(list(HandicraftCategory)).name
                ],
                credit_card_number="1234567890123456",
                status=random.choice(list(PostStatus))
            )
            session.add(post)
            posts.append(post)

        await session.flush()

        # Створюємо 30 відгуків
        for i in range(30):
            review = Review(
                user_id=random.choice(users).id,
                post_id=random.choice(posts).id,
                message=random.choice([
                    "Супер!", "Гарно зроблено", "Дуже сподобалося", "Рекомендую!", "Якість на висоті"
                ]),
                rating=random.randint(3, 5)
            )
            session.add(review)

        # Додаємо 30 обраних постів (favorites)
        favorites_set = set()
        while len(favorites_set) < 30:
            user = random.choice(users)
            post = random.choice(posts)
            key = (user.id, post.id)
            if key not in favorites_set:
                favorites_set.add(key)
                favorite = Favorite(
                    user_id=user.id,
                    post_id=post.id
                )
                session.add(favorite)

        await session.commit()
        print("✅ Тестові дані успішно додано (10 юзерів, 30 постів, 30 відгуків, 30 обраних)")

async def init_models():
    """Initialize models."""
    logging.log(20, "Initialising models: %s", models)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_database():
    """Initialize database"""
    await init_models()


@app.on_event("startup")
async def on_startup():
    """Startup event."""
    await init_database()
    await create_test_data()

@app.on_event("shutdown")
async def on_shutdown():
    """Shutdown event."""