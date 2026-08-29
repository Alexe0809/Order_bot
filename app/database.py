from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import config
import asyncio
from sqlalchemy import  select

DATABASE_URL = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base ()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, nullable=False)
    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=func.now())

async def seed_products():
    async with async_session() as session:
        session.add_all([
            Product(name='Iphone', price=43342),
            Product(name='Laptop', price=3245),
            Product(name='Apple', price=3454),
            Product(name='Car', price=45678),
            Product(name='Plane', price=4378042)
        ])
        await session.commit()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_product_by_name(name):
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.name == name))
        return result.scalar_one_or_none()

if __name__ == '__main__':
    asyncio.run(create_tables())