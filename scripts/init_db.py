import asyncio
from app.core.database import engine, Base
from app.models.price import Price  
from app.models.average import MovingAverage

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente")

if __name__ == "__main__":
    asyncio.run(init_db())