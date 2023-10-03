from aiogram import Dispatcher, Bot, types, filters
from settings import TOKEN, ADMIN_USER_IDS
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from keyboards import get_standart_keyboard, get_admin_keyboard
from db import sessionmaker
from middlewares.db import DbSessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import text, select
from sqlalchemy.sql.functions import count as fn_count
from models import Clients, Services
import datetime
from sqlalchemy.exc import IntegrityError

bot = Bot(token=TOKEN, parse_mode='HTML')


dp = Dispatcher(storage=MemoryStorage()) # , storage=storage)
dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

# @dp.message(F.from_user.id.in_(ADMIN_USER_IDS), filters.Command('start'))
# async def manager_start(message: types.Message):
#     await message.answer('Доборое утро менеджер!', reply_markup=get_admin_keyboard())


async def new_app_admin(client):
    for user_id in ADMIN_USER_IDS:
            await bot.send_message(
                chat_id=int(user_id), 
                text=f"""
<b>Новая заявка на приём</b>
<u>Данные контакта:</u>
Фамилия, Имя: <b>{client.last_name} {client.first_name}</b>
Номер телефона: <b>{client.phone_number}</b>
-----
Пожалуйста, свяжитесь с человеком, оставивщим заявку в ближайшее время!
""", 
                parse_mode='HTML')


@dp.message(F.from_user.id.in_(ADMIN_USER_IDS), filters.Command('start'))
async def admin_start(message: types.Message, state: FSMContext):
    state.clear()
    await message.answer('test', reply_markup=get_admin_keyboard())



@dp.message(filters.Command('start'))
async def start(message: types.Message, session: Session):
    sql = fn_count(select(Clients.id).where(Clients.id==message.from_user.id))
    q = await session.execute(statement=sql)
    in_base = q.scalar() > 0
    await message.answer(f"Привет, {message.from_user.full_name}. Твой Telegram ID: {message.from_user.id}", reply_markup=get_standart_keyboard(in_base=in_base))


@dp.message(filters.Command('help'))
async def help(message: types.Message):
    await message.answer("Это бот для теста. Но потом он может стать началом мегапроекта для рабты с заказми из ресторанов!")


@dp.message(F.contact)
async def contact_accept(message: types.Message, session: Session):
    if message.from_user.id == message.contact.user_id:
        new_client = Clients(
                id=message.contact.user_id,
                created=datetime.datetime.now(),
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                phone_number=message.contact.phone_number
            )
        try:
            session.add(new_client)
            await session.commit()
        except IntegrityError:
            pass
        await new_app_admin(new_client)
        await message.answer("Ваша заявка принята!\nМастер свяжется с Вами в ближайшее время.", reply_markup=get_standart_keyboard(in_base=True))


@dp.message(F.text == 'Запись на приём')
async def new_app(message: types.Message, session: Session):
    sql = select(Clients).where(Clients.id==message.from_user.id)
    clt = await session.execute(statement=sql)
    client = clt.first()
    if client is None:
        await message.answer("Для записи к мастеру нужно поделиться своим контактом!\nДля этого, пожалуйста, нажмите на кнопку \"Запись на приём\" в меню бота", reply_markup=get_standart_keyboard(in_base=False))
        return 0
    await new_app_admin(client.Clients)
    await message.answer("Ваша заявка принята!\nМастер свяжется с Вами в ближайшее время.", reply_markup=get_standart_keyboard(in_base=True))


@dp.message(F.text == 'Список услуг')
async def service_list(message: types.Message, session: Session):
    s_list = await session.execute(statement=select(Services))
    s_list = s_list.fetchall()
    msg = '<b><u>Список услуг:</u></b>\n'
    for ind, srv in enumerate(s_list):
        msg += f'\n<b>{ind+1}. {srv.Services.title}</b>\n{srv.Services.description}\n<b>💸 Цена: </b>{srv.Services.cost} руб.\n'
    await message.answer(text=msg)


@dp.message()
async def test_func(message: types.Message):
    await message.delete()