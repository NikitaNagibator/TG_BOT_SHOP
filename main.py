import asyncio
import configparser
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# import yoomoney_payment ЗАМОРОЖЕННО до Получения ИП или Самозанятого
from data import Database
import keyboard as kb
import keyboard_inline as kbi

cfg = configparser.ConfigParser()
cfg.read("config.ini")

TOKEN = cfg["Telegram"]["bot_token"]

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = Database("database.db")


# <Ожидание>------------------------
class Form(StatesGroup):
    data_cost = State()
    screenshot = State()
    change_costs = State()
    buy = State()
    input_cost = State()
    like_dislike = State()
    feedback_scr = State()
    feedback = State()


# </Ожидание>------------------------

# <Мейн часть>------------------------
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    user__id = message.from_user.id
    if not db.user_exist(user_id=user__id):
        db.add_user_id_and_name(user_id=user__id, user_name=message.from_user.full_name)
        print("Новый пользователь добавлен в базу данных")
    else:
        print("Этот пользователь уже есть в базе данных")

    await message.answer(f"<b>Привет, {message.from_user.full_name}</b>! Если ты хочешь купить"
                         f" <b>ДЕШЕВО ЛЮБУЮ ПОДПИСКУ</b>, ты попал туда куда надо!😉\n\n"
                         f"P.S. У нас САМЫЕ НИЗКИЕ ЦЕНЫ на рынке🤭",
                         parse_mode="HTML")
    await main_menu(message, state)


@dp.message(F.text == "/menu")
@dp.message(F.text == "Меню")
async def main_menu(message: Message, state: FSMContext):
    db.del_feed_by_user_id(user_id=message.from_user.id)
    await state.clear()
    db.update_data_buy(user_id=message.from_user.id, new_data="")
    user__id = message.from_user.id
    if not db.check_admin_status(user_id=user__id):
        await message.answer(f"{message.from_user.full_name}, не будем тянуть! <b>Давай закупаться!</b>",
                             parse_mode="HTML",
                             reply_markup=kb.choice_goods_kb)
    else:
        await message.answer(f"{message.from_user.full_name}, не будем тянуть! <b>Давай закупаться!</b>",
                             parse_mode="HTML",
                             reply_markup=kb.choice_goods_for_admin_kb)


@dp.message(F.text == "Назад")
@dp.message(F.text == "Выбрать товар")
async def choise_goods(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"<b>У нас огромный выбор!</b> Давай выбирай!",
                         parse_mode="HTML", reply_markup=kbi.goods_kbi)


# </Мейн часть>--------------------------------------------------

# <Админ-панель>--------------------------------------------------
@dp.message(F.text == "Админ-панель")
async def admin_panel(message: Message, state: FSMContext):
    user__id = message.from_user.id
    await state.clear()
    if db.check_admin_status(user_id=user__id):
        await message.answer("Это админ-панель!", reply_markup=kb.admin_panel_kb)
    else:
        await message.answer("<b>У Вас нет доступа к этой комадне!</b>", "HTML")


# </Админ-панель>-------------------------------------------------

# <Отзывы>--------------------------------------------------------
@dp.message(F.text == "Отзывы")
async def feedback_menu(message: Message, state: FSMContext):
    if db.get_10_feedback() != "ПУСТО":
        for data in db.get_10_feedback():
            if data[4] is None:
                await message.answer(f'"{data[3]}"\n@{data[2]}', reply_markup=kb.feedback_kb)
            else:
                await message.answer_photo(photo=data[4], caption=f'"{data[3]}"\n@{data[2]}', reply_markup=kb.feedback_kb)
    else:
        await message.answer("<b>Оставте первый отзыв!</b>", reply_markup=kb.feedback_kb, parse_mode="HTML")


@dp.message(F.text == "Оставить")
async def to_feedback(message: Message, state: FSMContext):
    await message.answer(
        "Сначала скиньте скриншот или нажмите пропустить\nДалее напишите отзыв\nИ в конце концов нажмите ОСТАВИТЬ!")
    await message.answer("Все давай, жду скриншот!", reply_markup=kb.feedback_scr_kb)
    await state.set_state(Form.feedback_scr)


@dp.message(Form.feedback_scr)
async def feedback_scr(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    db.add_feed(user_id=user_id, user_name=user_name)
    if message.photo:
        db.update_feed_scr(screen=message.photo[-1].file_id, user_id=user_id)
        await message.answer("Скриншот принят, жду пока вы напишите отзыв!", reply_markup=kb.menu_kb)
        await state.clear()
        await state.set_state(Form.feedback)
    elif message.text == "Пропустить":
        await message.answer("Тогда жду пока вы напишите отзыв!", reply_markup=kb.menu_kb)
        await state.clear()
        await state.set_state(Form.feedback)
    else:
        await message.answer("А-у-у-у, скриншот скинь \nИли вернись в /menu")


@dp.message(Form.feedback)
async def feedback_add(message: Message, state: FSMContext):
    if message.text == 'Меню':
        await main_menu(message, state)
        db.del_feed_by_user_id(user_id=message.from_user.id)
    elif message.text == 'Пропустить':
        await message.answer(f"ТАК НЕЛЬЗЯ!")
    elif message.text and 150 >= len(message.text) >= 5:
        db.update_feed(feedback=message.text,user_id=message.from_user.id)
        db.add_feedback(user_id=message.from_user.id)
        db.del_feed_by_user_id(user_id=message.from_user.id)
        await message.answer(f"Отлично! Спасибо за отзыв!")
        await main_menu(message,state)
        await state.clear()
    elif message.text:
        await message.answer("Ваш отзыв слишком короткий или слишком длинный!")
    else:
        await message.answer("Введите текстовый отзыв!"
                             "\nИли вернись в /menu")


# </Отзывы>-------------------------------------------------------


# <Яндекс> --------------------------------------------------------------------------------------------
@dp.callback_query(F.data == "ЯПлюс")
async def yandex(call: CallbackQuery):
    await call.message.answer_photo(photo="https://www.digiseller.ru/preview/147467/p1_3425937_ea806abc.jpg",
                                    caption="Вы выбрали <b>Яндекс Плюс!</b>",
                                    parse_mode="HTML", reply_markup=kbi.choise_yandex_kbi)
    await call.answer()


@dp.callback_query(F.data == "ЯПлюс_3мес")
async def yandex_3mes(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Яндекс Плюс</b> на <b>3 месяца</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_yandex_3_kbi)
    await call.answer()


@dp.callback_query(F.data == "ЯПлюс_6мес")
async def yandex_6mes(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Яндекс Плюс</b> на <b>6 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_yandex_6_kbi)
    await call.answer()


@dp.callback_query(F.data == "ЯПлюс_12мес")
async def yandex_12mes(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Яндекс Плюс</b> на <b>12 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_yandex_12_kbi)
    await call.answer()


# </Яндекс>-----------------------------------------------------------------------------------------------------

# <Дискорд>-----------------------------------------------------------------------------------------------------
@dp.callback_query(F.data == "DSNitro")
async def discord(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer_photo(photo="https://www.digiseller.ru/preview/1074943/p1_3360950_2f2a4b46.jpg",
                                    caption="Вы выбрали <b>Discord Nitro!</b>",
                                    parse_mode="HTML", reply_markup=kbi.choise_discord_kbi)
    await call.answer()


@dp.callback_query(F.data == "Dis_3мес")
async def yandex_3m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Discord Nitro</b> на <b>3 месяца</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_discord_3_kbi)
    await call.answer()


@dp.callback_query(F.data == "Dis_6мес")
async def yandex_6m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Discord Nitro</b> на <b>6 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_discord_6_kbi)
    await call.answer()


@dp.callback_query(F.data == "Dis_12мес")
async def yandex_12m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Discord Nitro</b> на <b>12 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_discord_12_kbi)
    await call.answer()


# </Дискорд>-----------------------------------------------------------------------------------------------------------

# <Спотифай>----------------------------------------------------------------------------------------------------
@dp.callback_query(F.data == "Spotify")
async def spotify(call: CallbackQuery):
    await call.message.answer_photo(
        photo="https://mygiftcard.ru/upload/iblock/334/3342b2078932d0016930faacc78ec248.png",
        caption="Вы выбрали <b>Spotify Premium!</b>",
        parse_mode="HTML", reply_markup=kbi.choise_spotify_kbi)
    await call.answer()


@dp.callback_query(F.data == "SP_3мес")
async def yandex_3m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Spotify Premium</b> на <b>3 месяца</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_spotify_3_kbi)
    await call.answer()


@dp.callback_query(F.data == "SP_6мес")
async def yandex_6m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Spotify Premium</b> на <b>6 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_spotify_6_kbi)
    await call.answer()


@dp.callback_query(F.data == "SP_12мес")
async def yandex_12m(call: CallbackQuery):
    db.update_data_buy(user_id=call.from_user.id, new_data=call.data)
    await call.message.answer("Вы выбрали <b>Spotify Premium</b> на <b>12 месяцев</b>", parse_mode="HTML",
                              reply_markup=kbi.buy_spotify_12_kbi)
    await call.answer()


# </Спотифай>----------------------------------------------------------------------------------------------------------

# <>-----------------------------------------------------------------------------------------------------------
@dp.callback_query(F.data == "Оплата")
async def buy(call: CallbackQuery, state: FSMContext):
    user__id = call.from_user.id
    if db.get_subs_code_by_data(data=db.check_data_buy(user_id=user__id)) != "Нет данной подписки" or db.get_subs_code_by_data(data=db.check_data_buy(user_id=user__id)) == "Нет данной подписки":
        await asyncio.sleep(1)
        await call.message.answer(
            f"Технические неполадки! ЮКасса сейчас недоступна, придется осуществить покупку переводом!")
        await call.message.answer(
            f"Мы решаем проблему, секундочку!")
        await asyncio.sleep(4)
        await call.message.answer(
            f"Вы выбрали: <u><b>{db.check_goods_with_data(data=db.check_data_buy(user_id=user__id))}</b></u>\n\n"
            f"Скиньте <b><u>{db.check_price_with_data(data=db.check_data_buy(user_id=user__id))} рублей </u></b>"
            f"по номеру карты:\n\n"
            f"<code><b>{cfg['Card']['number_of_card']}</b></code> \n\n"
            f"После оплаты скиньте мне скриншот!", "HTML")
        await state.set_state(Form.screenshot)
        await call.answer()
    else:
        await call.message.answer(
            f"Извините, но данная подписка закончилась, пожалуйста"
            " подождите час или выберите другую подписку!")
        await call.answer()
        db.add_ne_hvatilo_subs(user_id=user__id, data=db.check_data_buy(user_id=user__id))
        for admin_id in db.get_all_admin_status():
            await bot.send_message(chat_id=admin_id[0],
                                   text=f"<b>{db.count_ne_hvatilo()} людям не хватило подписки!</b>", parse_mode="HTML")
        await choise_goods(call.message, state)


@dp.message(Form.screenshot)
async def wait_screenshot(message: Message):
    if message.photo:
        user__id = message.from_user.id
        screenshot = message.photo[-1].file_id
        db.add_data_to_goods(user_id=user__id,
                             goods_name=db.check_goods_with_data(data=db.check_data_buy(user_id=user__id)),
                             goods_cost=db.check_price_with_data(data=db.check_data_buy(user_id=user__id)),
                             screensh=screenshot, user_name=message.from_user.full_name)
        await message.answer("В течение часа мы проверим оплату и отправим вам подписку")
        await message.answer(
            f"{message.from_user.full_name}, извините за временные неудобства, мы усердно стараемся ускорить нашу "
            f"работу!")
    else:
        await message.answer("А-у-у-у, скриншот скинь \nИли вернись в /menu")


# </>------------------------------------------------------------


# <Вкл/Выкл АДМИНКУ>---------------------------------------------
@dp.message(F.text == "/i_am_an_admin")
async def admin_status_on(message: Message, state: FSMContext):
    user__id = message.from_user.id
    db.admin_status_on(user_id=user__id)
    await message.answer("<b>Вы стали админом!</b>", parse_mode="HTML")
    await main_menu(message, state)


@dp.message(F.text == "/check_status")
async def check_status(message: Message):
    user__id = message.from_user.id
    if db.check_admin_status(user_id=user__id):
        await message.answer("Ваш статус: <b>Админ</b>", parse_mode="HTML")
    else:
        await message.answer("Ваш статус: <b>Пользователь</b>", parse_mode="HTML")


# </Вкл/Выкл АДМИНКУ>---------------------------------------------

# <Настройка цен>-------------------------------------------------
@dp.message(F.text == "Настройка цен")
async def change_costs(message: Message):
    await message.answer("Это настройка цен!", reply_markup=kbi.change_costs_kbi)


# ------
@dp.callback_query(F.data == "Yandex_change")
async def yandex_change_costs(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Вы выбрали <b>Яндекс Плюс</b>,\nВыберите план подписки", 'HTML',
                              reply_markup=kbi.yandex_change_costs_kbi)
    await state.set_state(Form.change_costs)
    await call.answer()


@dp.callback_query(F.data == "Яндекс Плюс 3 месяца")
async def yandex3_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Яндекс Плюс 3 месяца")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Яндекс Плюс 6 месяцев")
async def yandex6_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Яндекс Плюс 6 месяцев")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Яндекс Плюс 12 месяцев")
async def yandex12_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Яндекс Плюс 12 месяцев")
    await change_costs(call.message, state)
    await call.answer()


# -----

# -----
@dp.callback_query(F.data == "Discord_change")
async def discord_change_costs(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Вы выбрали <b>Discord Nitro</b>,\nВыберите план подписки", 'HTML',
                              reply_markup=kbi.discord_change_costs_kbi)
    await state.set_state(Form.change_costs)
    await call.answer()


@dp.callback_query(F.data == "Discord 3 месяца")
async def discord3_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Discord 3 месяца")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Discord 6 месяцев")
async def discord6_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Discord 6 месяцев")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Discord 12 месяцев")
async def discord12_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Discord 12 месяцев")
    await change_costs(call.message, state)
    await call.answer()


# -----

# -----
@dp.callback_query(F.data == "Spotify_change")
async def spotify_change_costs(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Вы выбрали <b>Spotify</b>,\nВыберите план подписки", 'HTML',
                              reply_markup=kbi.spotify_change_costs_kbi)
    await state.set_state(Form.change_costs)
    await call.answer()


@dp.callback_query(F.data == "Spotify Premium 3 месяца")
async def spotify3_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Spotify Premium 3 месяца")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Spotify Premium 6 месяцев")
async def spotify6_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Spotify Premium 6 месяцев")
    await change_costs(call.message, state)
    await call.answer()


@dp.callback_query(F.data == "Spotify Premium 12 месяцев")
async def spotify12_change_costs(call: CallbackQuery, state: FSMContext):
    # Устанавливаем выбранное значение плана в объект state
    await state.update_data(chosen_plan="Spotify Premium 12 месяцев")
    await change_costs(call.message, state)
    await call.answer()


# -----
@dp.message(Form.change_costs)
async def change_costs(message: Message, state: FSMContext):
    # Извлекаем выбранный план из объекта state
    data = await state.get_data()
    chosen_plan = data.get("chosen_plan", "Не выбрано")
    await message.answer(f"Вы выбрали план: <b>{chosen_plan}. Цена сейчас ({db.check_price(chosen_plan)}) </b> ",
                         "HTML")
    await message.answer(f"Введите новою цену:")
    await state.set_state(Form.input_cost)


@dp.message(Form.input_cost)
async def input_costa(message: Message, state: FSMContext):
    data = await state.get_data()
    chosen_plan = data.get("chosen_plan", "Не выбрано")
    try:
        if isinstance(int(message.text), int):
            db.update_price(name_goods=chosen_plan, new_price=message.text)
            await message.answer(f"Цена на <b>{chosen_plan}</b> успешно изменина на <b>{message.text} руб.</b>", "HTML")
            await state.clear()
            await main_menu(message, state)
    except:
        await message.answer(f"Введите цену коректно, а не {message.text}")


# </Настройка цен>------------------------------------------------

# <Проверка покупки>----------------------------------------------
@dp.message(F.text == "Проверка")
async def proverka(message: Message, state: FSMContext):
    user__id = message.from_user.id
    if not db.check_admin_status(user_id=user__id):
        await message.answer("У Вас нет прав для исполнения этой команды!")
    else:
        await message.answer(f"{message.from_user.full_name}, <b>давай проверять покупки!</b>",
                             parse_mode="HTML")
        await process_oplata_check(message, state)


async def process_oplata_check(message: Message, state: FSMContext):
    try:
        goods_id = db.get_id()
        goods_data = db.get_goods_by_id(goods_id)
        user_id, user_name, goods_name, screenshot, cost = goods_data
        caption = f"User ID: <code>{user_id}</code>\nИмя пользователя: <b>{user_name}</b>\n" \
                  f"Название товара: <b>{goods_name}</b>\nЦена: <b>{cost} руб</b>"

        await message.answer_photo(photo=screenshot, caption=caption, parse_mode="HTML",
                                   reply_markup=kb.like_dislike_kb)
        await state.set_state(Form.like_dislike)
    except:
        await message.answer("Вы проверили все оплаты!")
        await state.clear()
        await main_menu(message, state)


@dp.message(Form.like_dislike)
async def otsenka(message: Message, state: FSMContext) -> None:
    if message.text == "Меню":
        await main_menu(message)
        await state.clear()
    elif message.text == "👍":
        await process_oplata_approval(message, state)
        await process_oplata_check(message, state)
    elif message.text == "👎":
        await process_oplata_dislike(message, state)
        await process_oplata_check(message, state)


async def process_oplata_approval(message: Message, state: FSMContext):
    try:
        goods_id = db.get_id()
        goods_data = db.get_goods_by_id(goods_id)
        user_id, user_name, goods_name, screenshot, cost = goods_data

        code = db.get_subs_code_by_data(data=db.check_data_buy(user_id=user_id))

        db.add_to_approved_goods(screensh=screenshot, user_name=user_name, user_id=user_id, goods_name=goods_name,
                                 goods_cost=cost)

        await bot.send_message(chat_id=user_id,
                               text=f"<b>{user_name}</b>, вот Ваш код для активации <b>{goods_name}</b>:\n<code>"
                                    f"<b>{code}</b></code>", parse_mode="HTML")
        db.del_subs_code_by_code(code=code)
        db.del_goods_by_id(goods_id)
        await message.answer("Оплата подтверждена!")

    except:
        await message.answer("Вы проверили все оплаты!")
        await state.clear()
        await main_menu(message, state)


async def process_oplata_dislike(message: Message, state: FSMContext):
    try:
        goods_id = db.get_id()
        db.del_goods_by_id(goods_id)
        await message.answer("Оплата не подтверждена!")
    except:
        await message.answer("Вы проверили все оплаты!")
        await state.clear()
        await main_menu(message, state)


# </Проверка покупки>---------------------------------------------


# <Я тебя не понимаю>---------------------------------------------
@dp.message()
async def ya_hz(message: Message):
    await message.answer("<b>Я тебя не понимаю...</b>", parse_mode="HTML")


# </Я тебя не понимаю>---------------------------------------------


# <Запуск!>-------------------------------------------------------
async def main():
    print("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
