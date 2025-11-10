
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from subscriptions import add_subscription, is_subscription_active
from dotenv import load_dotenv
import os

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Trading Bot!\n"
        "/plans - View subscription plans\n"
        "/status - Check your subscription status\n"
        "/paid <tx_hash> - Activate your subscription"
    )

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Subscription Plans:\n"
        "- 1 Month: 0.1 BTC\n"
        "- 3 Months: 0.25 BTC\n"
        "Send the payment to <YOUR_BTC_ADDRESS> and use /paid <tx_hash> to activate."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if is_subscription_active(chat_id):
        await update.message.reply_text("Your subscription is active.")
    else:
        await update.message.reply_text("You do not have an active subscription.")

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    # tx_hash = context.args[0] if context.args else None
    # In a real scenario, you would verify the transaction hash
    add_subscription(chat_id)
    await update.message.reply_text("Your subscription has been activated for 30 days!")

def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plans", plans))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("paid", paid))
    
    app.run_polling()

if __name__ == "__main__":
    main()
