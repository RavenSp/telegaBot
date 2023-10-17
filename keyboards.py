from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_standart_keyboard(in_base: bool = False):
    kb = [[KeyboardButton(text='Список услуг'), KeyboardButton(text='Запись на приём', request_contact=not in_base)]]
    # keyboard.add(*['Список услуг', 'Запись на приём'])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Выберите действие')
    return keyboard


def get_admin_keyboard():
    kb = [
        [KeyboardButton(text='Список услуг'), KeyboardButton(text='Добавить услугу')],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def get_cancel_kb():
    kb = [[KeyboardButton(text='❌ Отмена')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

