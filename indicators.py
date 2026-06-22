# indicators.py
import numpy as np
import pandas as pd

def calculate_wilders_indicators(df):
    # คำนวณ True Range และ ATR
    df['Prev_Close'] = df['Close'].shift(1)
    df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum((df['High'] - df['Prev_Close']).abs(), (df['Low'] - df['Prev_Close']).abs()))
    df['ATR'] = df['TR'].ewm(alpha=1/14, adjust=False).mean()

    # คำนวณ ADX
    df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), np.maximum(df['High'] - df['High'].shift(1), 0), 0)
    df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), np.maximum(df['Low'].shift(1) - df['Low'], 0), 0)
    df['Smoothed_+DM'] = df['+DM'].ewm(alpha=1/14, adjust=False).mean()
    df['Smoothed_-DM'] = df['-DM'].ewm(alpha=1/14, adjust=False).mean()
    df['Smoothed_TR'] = df['TR'].ewm(alpha=1/14, adjust=False).mean()

    df['+DI'] = 100 * (df['Smoothed_+DM'] / (df['Smoothed_TR'] + 1e-8))
    df['-DI'] = 100 * (df['Smoothed_-DM'] / (df['Smoothed_TR'] + 1e-8))
    df['DX'] = 100 * ((df['+DI'] - df['-DI']).abs() / (df['+DI'] + df['-DI'] + 1e-8))
    df['ADX'] = df['DX'].ewm(alpha=1/14, adjust=False).mean()

    # คำนวณ EMA และ RSI
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / (loss + 1e-8))))
    
    df.dropna(subset=['ADX', 'EMA_200', 'RSI'], inplace=True)
    return df