from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_kb():
    kb_list = [
        [KeyboardButton(text="🤗 Добавить почту"), KeyboardButton(text="😢 Удалить почту")],
        [KeyboardButton(text="📝 Инструкция")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard