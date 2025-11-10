
import pandas as pd

def calculate_position_size(capital, risk_per_trade, stop_loss_price, entry_price):
    risk_amount = capital * risk_per_trade
    position_size = risk_amount / (entry_price - stop_loss_price)
    return position_size

def kill_switch(drawdown_threshold, current_drawdown):
    if current_drawdown > drawdown_threshold:
        # Here you might want to log, notify, or halt trading
        print(f"Kill switch triggered: Drawdown {current_drawdown} exceeds threshold {drawdown_threshold}")
        return True
    return False
