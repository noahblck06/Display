from sense_hat import SenseHat
import yfinance as yf
import time

sense = SenseHat()

# 🔧 Aktien-Ticker hier festlegen
TICKER = "AAPL"
UPDATE_INTERVAL = 240  # 4 Minuten

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    current_price = info['regularMarketPrice']
    previous_close = info['previousClose']
    change = current_price - previous_close
    return current_price, change

def scroll_price_message(price, symbol):
    message = f"{symbol}: ${price:.2f}"
    sense.show_message(message, scroll_speed=0.05, text_colour=[255, 255, 255])

def draw_chart(upward=True):
    sense.clear()
    color = [0, 255, 0] if upward else [255, 0, 0]
    heights = [1, 2, 3, 4, 5, 6, 7, 8] if upward else [8, 7, 6, 5, 4, 3, 2, 1]

    for x in range(8):
        for y in range(8 - heights[x], 8):
            sense.set_pixel(x, y, color)

def main():
    last_price = None
    last_change = None
    last_update = 0

    while True:
        current_time = time.time()

        if current_time - last_update > UPDATE_INTERVAL or last_price is None:
            try:
                last_price, last_change = get_stock_data(TICKER)
                last_update = current_time
            except Exception as e:
                sense.show_message("Fehler", text_colour=[255, 0, 0])
                print(e)
                time.sleep(10)
                continue

        # 💬 Scrollender Preistext
        scroll_price_message(last_price, TICKER)

        # 📊 Chart anzeigen
        draw_chart(upward=(last_change >= 0))

        # ⏳ Kurze Pause, damit Chart sichtbar bleibt
        time.sleep(5)

main()
