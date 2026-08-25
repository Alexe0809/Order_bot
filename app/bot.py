from config import BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import products_keyborard
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

class OrderForm(StatesGroup):
    name= State()
    quantity=State()
    phone=State()

@dp.message(CommandStart())
async def start_handler(message:Message):
    await message.answer(
        "Hello! How can I help you", 
        reply_markup=products_keyborard())

@dp.callback_query(F.data.startswith('product_'))
async def product_chosen(callback:CallbackQuery, state: FSMContext):
    product = callback.data.replace('product_', '')
    await callback.message.answer(f'You have choosed:{product}')
    await state.update_data(product=product)
    await state.set_state(OrderForm.quantity)
    await callback.message.answer('How much ?')
    await callback.answer()

@dp.message(OrderForm.quantity)
async def quantity_entered(message:Message, state:FSMContext):
    await state.update_data(quantity=message.text)
    await state.set_state(OrderForm.name)
    await message.answer('What is your name ?')

@dp.message(OrderForm.name)
async def name_entered(message:Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    await message.answer('What is your phine ?')

@dp.message(OrderForm.phone)
async def phone_entered(message:Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(f"Product: {data['product']}\nQuantity: {data['quantity']}\nName: {data['name']}\nPhone: {data['phone']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())