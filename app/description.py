from app import keyboard
from app import SQlite
from aiogram.utils.markdown import hbold

"""------------------------------<<<ПЕРЕМЕННЫЕ>>>------------------------------"""

set_1 = "Для покупки выберите интересующий сервер. " \
        "После оплаты вы мгновенно получите данные для подключения.\n\n- на первую покупку " \
        "скидка 20% по купону –☁️OBLAKA☁️(активировать купон можно в \"Мой профиль\")\n-произвольную конфигурацию вы можете заказать у нас " \
        "на сайте msk.oblaka.tech"
set_2 = f"Промокод по слову☁️ OBLAKA ☁️отнимает 20% от стоимости 1 пункта!\nЗайдите в свой профиль и активируйте его!"
set_3 = "Введите ваш промокод🎁"
set_4 = "☁️Надежное персональное облакои выделенные сервера по выгодным ценам💸\n\n🖥Максимальная производительность за " \
        "минимальные деньги\n\n👨‍💼 Услуги которые входят в стоимость обслуживания:\n1.📚 Регулярные резервные копии;\n" \
        "2.👷‍♂️Любой тариф обсуждается индивидуально под ваши задачи и ценовую политику;\n3.🔧Предустановленные любые " \
        "системы Windows/Linux;\n4.☁️Облачная 1С.\n\n💽 Возможны любые конфигурации памяти и дисков.\n\n📡 Поможем " \
        "организовать безопасное и анонимное подключение, развернуть ИТ - сервисы с нуля."
set_5 = "При дополнительных вопросах о серверах, можете обращаться в тех. поддержку📞"
referal = "💼 Реферальная система\n🎯 Реферальный процент: 10%\n💰 За приглашенных людей, которые оплатят товар " \
          "в нашем магазине вы получите 10% скидки от стоимости товара\n🌐 Для приглашения пользователей отправьте ваш " \
          "реферальный код! Или введите реферальный код пользователя, который вас пригласил."
error = "Ой-ой...4️⃣0️⃣4️⃣ Ошибочка вышла"
input_referal = "Отправьте, пожалуйста, реферальный код пользователя, который вас пригласил!🤝"
servers = {
        "serv_0":["🇷🇺","4","8","2400"],
        "serv_1":["🇷🇺","6","16","4000"],
        "serv_2":["🇷🇺","8","24","5500"],
        "serv_3":["🇷🇺","10","32","7000"],
        "serv_4":["🇵🇱","4","8","2400"],
        "serv_5":["🇵🇱","6","16","4000"],
        "serv_6":["🇵🇱","8","24","5500"],
        "serv_7":["🇵🇱","10","32","7000"],
        "serv_8":["🇺🇸","4","8","2400"],
        "serv_9":["🇺🇸","6","16","4000"],
        "serv_10":["🇺🇸","8","24","5500"],
        "serv_11":["🇺🇸","10","32","7000"]
           }
activate_coupon_string = "Ваш купон активирован!"
user_have_no_coupon = "Ваш купон☁️OBLAKA ☁️уже был активирован"
bad_referal_code = "К сожалению такого аккаунта не существует, или вы ввели неправильный реферальный код😬"

"""------------------------------<<<ФУНКЦИИ ДЛЯ РАСЧЕТА>>>------------------------------"""

def text(choose, string_):
        answer = string_ + \
           f"\nЦена: {servers.get(choose)[3]}р\n\n" \
           f"ОС: Windows (по запросу любую ОС)\n" \
           f"Ядра: {servers.get(choose)[1]} Ядра х 2.5-4.0 GHz\n" \
           f"ОЗУ: {servers.get(choose)[2]} ГБ\n" \
           f"Интернет: 1 Гб/с\n" \
           f"SSD: 128 Гб\n" \
           f"Локация: Россия Москва"
        return answer

def buy_server(choose):
    answer = f"{keyboard.s_d.get(choose)[0]}{keyboard.s_d.get(choose)[1]} Ядра (2.5-4.0 GHz) | " \
    f"{keyboard.s_d.get(choose)[2]} озу | 128 ssd | {keyboard.s_d.get(choose)[3]}P"
    return answer


def text_my_profile(name, id, purchases, money):
    answer = f"Профиль {hbold(name)} c айди {hbold(id)}\nВсего покупок: {purchases}\nБаланс: {money}₽"
    return answer


def is_user(users, referal, id):
    referal = referal.replace("rf","")
    try:
        for user in users:
            user = list(user)
            if int(user[1]) == int(referal) and int(user[1]) != int(id):
                return True
    except:
        return False
    return False

def check_coupon_in_db(user, id):
    if int(user) == 1: #Проверка в БД на наличие купона
        SQlite.add_discount_oblaka(id)
        text = activate_coupon_string
    elif int(user) == 0: text = user_have_no_coupon
    else: text = error
    return text

def information_about_server(choose):
    if choose == "back_to_choose":
        tex = set_1
        reply_markup = keyboard.servers.as_markup()
        return tex, reply_markup
    buy_serv = buy_server(choose)
    tex = text(choose, buy_serv)
    reply_markup = keyboard.inline_keyboard_in_choose(choose, buy_serv)
    return tex, reply_markup

def check_referal_discount(id):
    db = SQlite.all_telegram_id()
    user = SQlite.user_info(id)
    for name in db:
        if str(name[12]) == str(id) and name[5] > 0 and str(name[1]) not in str(user[13]):
            SQlite.add_referal_discount(id)

            '''СТРОКИ НИЖЕ ДОЛЖНЫ ВЫПОЛНЯТЬСЯ ТОЛЬКО ПОСЛЕ ОПЛАТЫ!!!!!!!'''
            if name[13] == "no": user_invite = f"{str(name[1])}_"
            else: user_invite = f"{name[13]}{str(name[1])}_"
            SQlite.add_referal_discount_new_user(id, user_invite)


def buy_or_back(data, id):
    if data == "back_to_choosing_server":
        txt = set_1
        reply_markup = keyboard.servers.as_markup()
        return txt, reply_markup
    server_choose, discount = data.replace("buy_",""), "no"
    user_info = SQlite.user_info(id)
    price = int((servers.get(server_choose))[3])
    check_referal_discount(id)
    if int(user_info[7]) > 0 or int(user_info[8]) > 0:
        discount = max(int(user_info[7]), int(user_info[8]))
        price = price - (price * (discount/100))
        if int(user_info[7]) > int(user_info[8]): discount = "dis"
        else: discount = "ref"
    SQlite.server_choosing(discount, price, server_choose, id)
    txt = text(server_choose,"")
    txt = f"Вы выбрали: \n{txt}\n\nОкончательная цена: {hbold(str(price))}Р"
    reply_markup = keyboard.buy_from.as_markup()
    return txt, reply_markup

def my_profile(id, name):
    SQlite.add_new_user(id, name)
    user_info = SQlite.user_info(id)
    txt = text_my_profile(name, id, str(user_info[5]), str(user_info[3]))
    reply_markup = keyboard.my_profile.as_markup()
    return txt, reply_markup

def oblaka(id, name):
    SQlite.add_new_user(id, name)
    user_info = SQlite.user_info(id)
    txt = check_coupon_in_db(user_info[4], id)
    return txt

def activate_coupon(id, name):
    user_info = SQlite.user_info(id)
    txt = text_my_profile(name, id, str(user_info[5]), str(user_info[3]))
    reply_markup = keyboard.my_profile.as_markup()
    return txt, reply_markup

def admin_panel(name):
    txt = f"{name} добро пожаловать в админ панель!\nВыберите интересующие вас пункты:"
    reply_markup = keyboard.admin_panel.as_markup()
    return txt, reply_markup

def db_into_message():
    db = SQlite.all_telegram_id()
    message = "id | telegram_id | username | money \n"
    for user in db:
        x=0
        while x!=4:
            message += f" {str(user[x])} |"
            x+=1
        message += "\n"
    return message