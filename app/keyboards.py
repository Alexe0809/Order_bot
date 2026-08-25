from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def products_keyborard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Iphone', callback_data='product_Iphone')],
        [InlineKeyboardButton(text='Laptop', callback_data='product_Laptop')],
        [InlineKeyboardButton(text='Apple', callback_data='product_Applep')],
        [InlineKeyboardButton(text='Car', callback_data='product_Car')],
        [InlineKeyboardButton(text='Plane', callback_data='product_Plane')]
    ])