


from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse

from database.db import engine
from database.models import Base

from exceptions import NoLongUrlFoundError, SlugAlreadyExistsError
from service import generate_short_url, get_url_by_slug 


from database.crud import new_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)




async def get_session():
    async with new_session() as session:
        yield session


@app.post('/short_url')
async def generate_slug(
    long_url: str = Body(embed=True)
):
    try:
        new_slug = await generate_short_url(long_url)
    except SlugAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Не удалось сгенерировать slug')
        
    return {'data': new_slug}

@app.get('/{slug}')
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except NoLongUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не существует')
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)


