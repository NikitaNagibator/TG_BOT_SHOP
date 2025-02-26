from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Обычная клавиатура
choice_goods = [
    [KeyboardButton(text="Выбрать товар"),
     KeyboardButton(text="Отзывы"),
     KeyboardButton(text="Назад"),
     ],
]

choice_goods_for_admin = [
    [KeyboardButton(text="Выбрать товар"),
     KeyboardButton(text="Отзывы"),
     KeyboardButton(text="Назад"),
     ],
    [KeyboardButton(text="Админ-панель"),
     ],
]

like_dislike = [
    [KeyboardButton(text="👍"),
     KeyboardButton(text="👎"),
     ],
    [KeyboardButton(text="Меню"),
     ],
]

admin_panel = [
    [KeyboardButton(text="Проверка"),
     KeyboardButton(text="Отзывы"),
     KeyboardButton(text="Настройка цен"),
     ],
    [KeyboardButton(text="Меню"),
     ],

]

feedback = [
    [KeyboardButton(text="Оставить"),
     ],
    [KeyboardButton(text="Меню"),
     ],
]

feedback_scr = [
    [KeyboardButton(text="Пропустить"),
     ],
    [KeyboardButton(text="Меню"),
     ],

]

menu_m = [[KeyboardButton(text="Меню")],]

admin_panel_kb = ReplyKeyboardMarkup(keyboard=admin_panel,
                                      resize_keyboard=True,
                                      input_field_placeholder='Выбирай чо делать')

feedback_kb = ReplyKeyboardMarkup(keyboard=feedback,
                                      resize_keyboard=True,
                                      input_field_placeholder='Выбирай чо делать')

feedback_scr_kb = ReplyKeyboardMarkup(keyboard=feedback_scr,
                                      resize_keyboard=True,
                                      input_field_placeholder='Выбирай чо делать')

choice_goods_kb = ReplyKeyboardMarkup(keyboard=choice_goods,
                                      resize_keyboard=True,
                                      input_field_placeholder='Выбирай чо делать')

choice_goods_for_admin_kb = ReplyKeyboardMarkup(keyboard=choice_goods_for_admin,
                                      resize_keyboard=True,
                                      input_field_placeholder='Выбирай чо делать')

menu_kb = ReplyKeyboardMarkup(keyboard= menu_m,
                            resize_keyboard=True,
                            input_field_placeholder='Выбирай чо делать')

like_dislike_kb = ReplyKeyboardMarkup(keyboard = like_dislike,
                            resize_keyboard=True,
                            input_field_placeholder='Выбирай чо делать')
