
from shortener import generate_random_slug
from database.crud import add_slug_to_database
from database.crud import get_long_url_by_slug_from_database
from exceptions import NoLongUrlFoundError, SlugAlreadyExistsError


async def generate_short_url(
    long_url: str, 
):
    # 1 герерим slug
    # 2 добавляем в базу 
    # 3 отдаем клиенту 
    
    async def _generate_slug_and_add_to_db():
        slug = generate_random_slug()
        await add_slug_to_database(
        slug, long_url)
        return slug
    
    for attempt in range(5):
        try:
            slug = await _generate_slug_and_add_to_db()
            return slug
        except SlugAlreadyExistsError as ex:
            if attempt == 4:
                raise SlugAlreadyExistsError from ex
    return slug


async def get_url_by_slug(slug:str) -> str:
    long_url = await get_long_url_by_slug_from_database(slug)
    if not long_url:
        raise NoLongUrlFoundError()
    return long_url