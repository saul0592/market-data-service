import asyncio
from app.core.database import engine, Base
from app.models.price import RawMarketData, ProcessedPricePoint, MovingAvarage, PollingJobConfig

async def init_db():
    async with engine.begin() as conn:
        # Esto crea las tablas en la base de datos si no existen
        await conn.run_sync(Base.metadata.create_all)

    print("Tablas creadas correctamente")

if __name__ == "__main__":
    asyncio.run(init_db())