
from telegram import Bot
from subscriptions import get_all_active_subscribers

async def send_message(bot: Bot, chat_id: int, message: str):
    await bot.send_message(chat_id=chat_id, text=message)

async def broadcast_message(bot: Bot, message: str):
    active_subscribers = get_all_active_subscribers()
    for chat_id in active_subscribers:
        await send_message(bot, chat_id, message)
