import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models.db_helper import db_helper
from core.models import Base
from api.crud.insert_data_in_tables import insert_data
from api.routes_users import users_route
from api.routes_tweets import tweets_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Если приложение будет перезапущено, все данные в базе данных
        будут перезаписаны в начальное значение, для этого и используется
        lifespan.
    """
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await insert_data(conn)
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(users_route)
main_app.include_router(tweets_route)


if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)
