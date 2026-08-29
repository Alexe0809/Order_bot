from sqlalchemy import  select

async def get_product_by_name(name):
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.name == name))
        return result.scalar_one_or_none()