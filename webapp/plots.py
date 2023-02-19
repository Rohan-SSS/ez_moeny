import matplotlib.pyplot as plt
plt.style.use("dark_background")

def plot_chart(df):
    width = 0.6   # width of real body
    width2 = 0.05  # width of shadow
    offset = 0.2  # offset between adjacent bars

    fig, ax = plt.subplots(figsize=(24, 12))

    # find the rows that are bullish
    dfup = df[df.close >= df.open]
    # find the rows that are bearish
    dfdown = df[df.close < df.open]

    # plot the bullish candle stick with an offset
    ax.bar(dfup.index - offset/2, dfup.close - dfup.open, width,
        bottom=dfup.open, edgecolor='w', color='green')
    ax.bar(dfup.index - offset/2, dfup.high - dfup.close, width2,
        bottom=dfup.close, edgecolor='w', color='green')
    ax.bar(dfup.index - offset/2, dfup.low - dfup.open, width2,
        bottom=dfup.open, edgecolor='w', color='green')

    # plot the bearish candle stick with an offset
    ax.bar(dfdown.index + offset/2, dfdown.close - dfdown.open, width,
        bottom=dfdown.open, edgecolor='w', color='red')
    ax.bar(dfdown.index + offset/2, dfdown.high - dfdown.open, width2,
        bottom=dfdown.open, edgecolor='w', color='red')
    ax.bar(dfdown.index + offset/2, dfdown.low - dfdown.close, width2,
        bottom=dfdown.close, edgecolor='w', color='red')
    ax.grid(color='gray')

    plt.plot(df.EMA_100, 'white')
    plt.plot(df.EMA_200, 'grey')
    plt.plot(df.VWAP, 'blue')


def plot_res(predictions, y):
    plt.figure(figsize=(30,4))
    plt.plot(predictions[:100], 'g')
    plt.plot((y[:100]),  'r')
    plt.axhline(y=0, color='black', linestyle='--')
    plt.show