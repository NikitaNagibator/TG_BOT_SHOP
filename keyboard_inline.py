from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import Database

db = Database("database.db")

# Варианты подписок

goods_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Яндекс Плюс", callback_data="ЯПлюс")
    ],
    [
        InlineKeyboardButton(text="Discord Nitro", callback_data="DSNitro")
    ],
    [
        InlineKeyboardButton(text="Spotify Premium", callback_data="Spotify")
    ],
])


#Описание товара ------------------------------------------------------------------------------------------
choise_yandex_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"3 месяца | {db.check_price(name_goods='Яндекс Плюс 3 месяца')} рублей", callback_data="ЯПлюс_3мес"),
        InlineKeyboardButton(text=f"6 месяца | {db.check_price(name_goods='Яндекс Плюс 6 месяцев')} рублей", callback_data="ЯПлюс_6мес")
    ],
    [
        InlineKeyboardButton(text=f"12 месяца | {db.check_price(name_goods='Яндекс Плюс 12 месяцев')} рублей", callback_data="ЯПлюс_12мес")
    ],
])


choise_discord_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"3 месяца | {db.check_price(name_goods='Discord 3 месяца')} рублей", callback_data="Dis_3мес"),
        InlineKeyboardButton(text=f"6 месяца | {db.check_price(name_goods='Discord 6 месяцев')} рублей", callback_data="Dis_6мес")
    ],
    [
        InlineKeyboardButton(text=f"12 месяца | {db.check_price(name_goods='Discord 12 месяцев')} рублей", callback_data="Dis_12мес")
    ],
])


choise_spotify_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"3 месяца | {db.check_price(name_goods='Spotify Premium 3 месяца')} рублей", callback_data="SP_3мес"),
        InlineKeyboardButton(text=f"6 месяца | {db.check_price(name_goods='Spotify Premium 6 месяцев')} рублей", callback_data="SP_6мес")
    ],
    [
        InlineKeyboardButton(text=f"12 месяца | {db.check_price(name_goods='Spotify Premium 12 месяцев')} рублей", callback_data="SP_12мес")
    ],
])

#---------------------------------------------------------------------------------------------------


#Переход к оплате Яндекс-----------------------------------------------------------------------------------------
buy_yandex_3_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Яндекс Плюс 3 месяца')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="ЯПлюс")
    ],
])

buy_yandex_6_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Яндекс Плюс 6 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="ЯПлюс")
    ],
])


buy_yandex_12_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Яндекс Плюс 12 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="ЯПлюс")
    ],
])
#Переход к оплате Яндекс-----------------------------------------------------------------------------------------

#Переход к оплате Дискорд-----------------------------------------------------------------------------------------

buy_discord_3_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Discord 3 месяца')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="DSNitro")
    ],
])

buy_discord_6_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Discord 6 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="DSNitro")
    ],
])


buy_discord_12_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Discord 12 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="DSNitro")
    ],
])

#Переход к оплате Дискорд-----------------------------------------------------------------------------------------

#Переход к оплате Спотифай-----------------------------------------------------------------------------------------
buy_spotify_3_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Spotify Premium 3 месяца')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="Spotify")
    ],
])

buy_spotify_6_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Spotify Premium 6 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="Spotify")
    ],
])


buy_spotify_12_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f"Купить за {db.check_price(name_goods='Spotify Premium 12 месяцев')}р", callback_data="Оплата"),
        InlineKeyboardButton(text="Отмена", callback_data="Spotify")
    ],
])
#Переход к оплате Спотифай-----------------------------------------------------------------------------------------

# Отказ от оплаты -------------------------------------------------------------------------------------------------
otkaz_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Я не хочу покупать", callback_data="to_menu"),
    ],
])

#----------------------------------------------------------------------------------------------

#Изменение_цен--------------------------------------------------------------------------------
change_costs_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Яндекс Плюс", callback_data="Yandex_change"),
    ],
    [
        InlineKeyboardButton(text="Discord Nitro", callback_data="Discord_change"),
    ],
    [
        InlineKeyboardButton(text="Spotify", callback_data="Spotify_change"),
    ],
])

yandex_change_costs_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="3 месяца", callback_data="Яндекс Плюс 3 месяца"),
    ],
    [
        InlineKeyboardButton(text="6 месяцев", callback_data="Яндекс Плюс 6 месяцев"),
    ],
    [
        InlineKeyboardButton(text="12 месяцев", callback_data="Яндекс Плюс 12 месяцев"),
    ],
])

discord_change_costs_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="3 месяца", callback_data="Discord 3 месяца"),
    ],
    [
        InlineKeyboardButton(text="6 месяцев", callback_data="Discord 6 месяцев"),
    ],
    [
        InlineKeyboardButton(text="12 месяцев", callback_data="Discord 12 месяцев"),
    ],
])

spotify_change_costs_kbi = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="3 месяца", callback_data="Spotify Premium 3 месяца"),
    ],
    [
        InlineKeyboardButton(text="6 месяцев", callback_data="Spotify Premium 6 месяцев"),
    ],
    [
        InlineKeyboardButton(text="12 месяцев", callback_data="Spotify Premium 12 месяцев"),
    ],
])