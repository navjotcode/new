
import pandas as pd
import pandas_ta as ta

def generate_signal(df, ema_short, ema_long, rsi_period, rsi_overbought, rsi_oversold, atr_period, atr_multiplier):
    # Calculate indicators
    df.ta.ema(length=ema_short, append=True)
    df.ta.ema(length=ema_long, append=True)
    df.ta.rsi(length=rsi_period, append=True)
    df.ta.atr(length=atr_period, append=True)

    # Strategy logic
    last_row = df.iloc[-1]
    previous_row = df.iloc[-2]

    signal = None
    stop_loss = None
    take_profit = None

    # Breakout condition
    if last_row[f'EMA_{ema_short}'] > last_row[f'EMA_{ema_long}'] and previous_row[f'EMA_{ema_short}'] <= previous_row[f'EMA_{ema_long}'] and last_row[f'RSI_{rsi_period}'] < rsi_overbought:
        signal = 'BUY'
        stop_loss = last_row['close'] - last_row[f'ATRr_{atr_period}'] * atr_multiplier
        take_profit = last_row['close'] + (last_row['close'] - stop_loss) * 1.5  # Example take profit

    elif last_row[f'EMA_{ema_short}'] < last_row[f'EMA_{ema_long}'] and previous_row[f'EMA_{ema_short}'] >= previous_row[f'EMA_{ema_long}'] and last_row[f'RSI_{rsi_period}'] > rsi_oversold:
        signal = 'SELL'
        stop_loss = last_row['close'] + last_row[f'ATRr_{atr_period}'] * atr_multiplier
        take_profit = last_row['close'] - (stop_loss - last_row['close']) * 1.5  # Example take profit

    return signal, stop_loss, take_profit

