from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.crud.insert_data_in_tables import insert_data
from src.api.routes_medias import medias_route
from src.api.routes_tweets import tweets_route
from src.api.routes_users import users_route
from src.core.models.model_base import Base
from src.core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Если приложение будет перезапущено, все данные в базе данных
    будут перезаписаны в начальное значение, для этого и используется
    lifespan. Чтобы не оставалось незакрытых подключений к БД.
    """
    # Для того чтобы создать таблицы и наполнить их
    # демонстрационными данными раскомментируйте ниже 4 строки.
    # Затем их можно снова закомментировать, чтобы база данных не
    # обнулялась.
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    #     await insert_data(conn)
    yield

    # закрывает все соединения и освобождает ресурсы после работы
    # с базой данных
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(users_route)
main_app.include_router(tweets_route)
main_app.include_router(medias_route)


if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)
