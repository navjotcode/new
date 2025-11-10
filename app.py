
import asyncio
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

from broker import Broker
from strategy import generate_signal
from notifier import broadcast_message
from dotenv import load_dotenv
import os

load_dotenv()

async def trading_loop(broker, bot, config):
    print("Fetching data...")
    ohlcv = await broker.fetch_ohlcv(config['strategy']['symbol'], config['strategy']['timeframe'])
    
    print("Generating signal...")
    signal, sl, tp = generate_signal(ohlcv, **config['strategy'])
    
    if signal:
        print(f"Signal: {signal}, SL: {sl}, TP: {tp}")
        message = f"New Signal for {config['strategy']['symbol']}: {signal} @ {ohlcv.iloc[-1]['close']}\nSL: {sl}\nTP: {tp}"
        if config['runtime']['mode'] == 'signal':
            await broadcast_message(bot, message)
        elif config['runtime']['mode'] == 'trade':
            # Trading logic would go here
            pass

async def main():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Initialize Broker and Bot
    broker = Broker(api_key=os.getenv("EXCHANGE_API_KEY"), api_secret=os.getenv("EXCHANGE_API_SECRET"))
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    # Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(trading_loop, 'interval', minutes=5, args=[broker, bot, config])
    scheduler.start()

    try:
        # Keep the script running
        while True:
            await asyncio.sleep(1)
    finally:
        await broker.close()
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
