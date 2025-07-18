import matplotlib.pyplot as plt

def plot_signals(df, title="Trade Signals"):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price')
    if 'MA_Short' in df: plt.plot(df['MA_Short'], label='Short MA')
    if 'MA_Long' in df: plt.plot(df['MA_Long'], label='Long MA')
    plt.plot(df[df['Position'] == 1].index, df[df['Position'] == 1]['Close'],
             '^', color='green', label='Buy Signal', markersize=10)
    plt.plot(df[df['Position'] == -1].index, df[df['Position'] == -1]['Close'],
             'v', color='red', label='Sell Signal', markersize=10)
    plt.legend()
    plt.title(title)
    plt.grid()
    plt.show()
