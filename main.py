import asyncio
import logging
import sys
import os
from app import keyboard, description, SQlite

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold


load_dotenv()
dp = Dispatcher()

SQlite.check_table()

# То что происходит при команде /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    text = SQlite.add_new_user(message.from_user.id, message.from_user.full_name)
    await message.answer(text, reply_markup=keyboard.builder.as_markup(resize_keyboard=True))

#Админ панель
@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if str(message.from_user.id) in os.getenv("ADMIN_IDS"):
        text, reply_markup = description.admin_panel(message.from_user.first_name)
        await message.answer(text, reply_markup=reply_markup)
    else: await message.reply("Я не понимаю тебя")

# То что происходит при вводе слова
@dp.message(F.text == "🖥VDS/VPS Сервера в наличии")
async def open_all_servers(message: types.Message):
    SQlite.add_new_user(message.from_user.id, message.from_user.first_name)
    await message.answer(description.set_1, reply_markup=keyboard.servers.as_markup())

# Информация о промокоде
@dp.message(F.text == "🎁Промокод")
async def info_promocode(message: types.Message):
    await message.answer(description.set_2)

# Профиль пользователя
@dp.message(F.text == "🙍‍♂️Мой профиль")
async def my_profile(message: types.Message):
    text, reply_markup = description.my_profile(message.from_user.id, message.from_user.first_name)
    await message.answer(text, reply_markup=reply_markup)

# Информация о компании
@dp.message(F.text == "ℹ️Информация")
async def information(message: types.Message):
    await message.answer(description.set_4)

# Контакты разработчика и тех.поддержки
@dp.message(F.text == "📞Контакты")
async def contacts(message: types.Message):
    await message.answer(description.set_5, reply_markup=keyboard.technical_support.as_markup())

# Вызывается, если пользователь вводит OBLAKA
@dp.message(F.text == "OBLAKA")
async def oblaka(message: types.Message):
    text = description.oblaka(message.from_user.id, message.from_user.first_name)
    await message.answer(text)


#Отклик на запрос информации по определенному серверу
@dp.callback_query(F.data.in_(keyboard.key_server_description))
async def callback_one_server(callback_query: types.callback_query):
    text, reply_markup = description.information_about_server(callback_query.data)
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


#Отклик на КУПИТЬ или Назад
@dp.callback_query(F.data.in_(keyboard.buy_))
async def callback_bue_or_back(callback_query: types.callback_query):
    text, reply_markup = description.buy_or_back(callback_query.data, callback_query.from_user.id)
    await callback_query.message.edit_text(text= text, reply_markup=keyboard.buy_from.as_markup())

#Ввод реферальной ссылки
@dp.callback_query(F.data.in_("input_referal"))
async def callback_referal_code(callback_query: types.callback_query):
    text, reply_markup = description.input_referal, keyboard.back_to_my_profile.as_markup()
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)

# КОД ДЛЯ ПОЛУЧЕНИЯ ОПЛАТЫ!!!
# @dp.callback_query(F.data.in_("buy"))
# async def callback_query_keyboard(callback_query: types.callback_query):
#     if server_choose == "":
#         return

#Отклик на нажатие callback кнопоки "Активировать купон" в "Мой профиль"
@dp.callback_query(F.data.in_("back_to_my_profile"))
async def callback_activate_coupon(callback_query: types.callback_query):
    text, reply_markup = description.activate_coupon(callback_query.from_user.id, callback_query.from_user.first_name)
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


#Отклик на нажатие callback кнопоки "Реферальная система" в "Мой профиль"
@dp.callback_query(F.data.in_("referal_system"))
async def callback_referal_system(callback_query: types.callback_query):
    text = description.referal + f"\n\nВаш реферальный код: rf{hbold(callback_query.from_user.id)}"
    rep_markup = keyboard.input_referal.as_markup()
    await callback_query.message.edit_text(text=text, reply_markup=rep_markup)


#Отклик на нажатие callback кнопоки "Активировать купон" в "Мой профиль"
@dp.callback_query(F.data.in_("coupon"))
async def callback_activate_coupon(callback_query: types.callback_query):
    text = description.set_3
    rep_markup = keyboard.back_to_my_profile.as_markup()
    await callback_query.message.edit_text(text=text, reply_markup=rep_markup)


#Отклик на нажатие admin кнопок"
@dp.callback_query(F.data.in_(["db_to_chat"]))
async def callback_activate_coupon(callback_query: types.callback_query):
    if callback_query.data == "db_to_chat": await callback_query.message.edit_text(text=description.db_into_message())


#Отклик на нажатие неизвестных callback кнопок
@dp.callback_query()
async def callback_unexpected_inline_button(callback_query: types.callback_query):
    text = description.error
    rep_markup=keyboard.back_to_my_profile.as_markup()
    await callback_query.message.edit_text(text=text, reply_markup=rep_markup)


# То что происходит при любом сообщении в чате, кроме прошлых ДОДЕЛАТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@dp.message()
async def unexpected_message(message: types.Message):
    if "rf" in message.text:
        all_users = SQlite.all_telegram_id()
        is_user = description.is_user(all_users, message.text, message.from_user.id)
        if is_user == False:
            await message.answer(text=description.bad_referal_code)
            return
        else:
            answer = SQlite.add_referal_to_user(message.text, message.from_user.id)
            await message.answer(text=answer)
    else: await message.reply("Я не понимаю тебя")


# Запуск этой машины
async def main():
    bot = Bot(os.getenv("TOKEN"), parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())