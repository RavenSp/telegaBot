from fastapi import FastAPI
from aiogram import types
from settings import ADMIN_USER_IDS
from bot import dp, bot, TOKEN
from db import engine
from models import Base, Services
from db import sessionmaker
from pydantic import BaseModel

app = FastAPI()
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = "https://firm-oddly-husky.ngrok-free.app" + WEBHOOK_PATH



@app.on_event("startup")
async def on_startup():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp._process_update(update=telegram_update, bot=bot)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


class ServiceScheme(BaseModel):

    title: str
    description: str
    cost: int


@app.post('/new-service')
async def new_service(service: ServiceScheme):
    async with sessionmaker() as session:
        session.add(Services(**service.dict()))
        await session.commit()
    return 'ok'