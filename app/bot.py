from config import BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import products_keyborard, confirm_keyboard
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import get_product_by_name, Order, async_session


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
    await message.answer('What is your phone ?')

@dp.message(OrderForm.phone)
async def phone_entered(message:Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    product = await get_product_by_name(data['product'])
    quantity = int(data['quantity'])
    total = product.price * quantity
    await state.update_data(product_id=product.id, price=product.price, total=total)
    await message.answer(
        f"Product: {product.name}\n"
        f"Quantity: {quantity}\n"
        f"Price: ${product.price}\n"
        f"Total: ${total}\n\n"
        f"Name: {data['name']}\n"
        f"Phone: {data['phone']}",
        reply_markup=confirm_keyboard()
    )


@dp.callback_query(F.data == 'confirm')
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'name' not in data:
        await callback.message.answer("Сессия устарела, начните заново: /start")
        await callback.answer()
        return
    async with async_session() as session:
        order = Order(
            telegram_user_id=callback.from_user.id,
            customer_name=data['name'],
            phone=data['phone'],
            product_id=data['product_id'],
            quantity=int(data['quantity']),
            price=data['price'],
            total=data['total'],
        )

        session.add(order)
        await session.commit()
        order_id=order.id

    await callback.message.answer(f'✅ Order №{order_id} successfully created! Total: ${data['total']}')
    await state.clear()
    await callback.answer()

@dp.callback_query(F.data == "cancel")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Order was cancelled")
    await callback.answer()


     
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())