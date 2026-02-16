from sense_hat import SenseHat
import yfinance as yf
import time

sense = SenseHat()

# Yahoo Aktien-Ticker hier festlegen
TICKER = "IWDA.AS"
UPDATE_INTERVAL = 240  # 4 Minuten

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    current_price = info['regularMarketPrice']
    previous_close = info['previousClose']
    change = current_price - previous_close
    return current_price, change

def scroll_price_message(price, symbol):
    message = f"{symbol}: EUR {price:.2f}"
    sense.show_message(message, scroll_speed=0.1, text_colour=[255, 255, 255])

def draw_chart(upward=True):
    sense.clear()
    color = [0, 255, 0] if upward else [255, 0, 0]
    heights = [0, 0, 0, 1, 2, 4, 6, 8] if upward else [8, 6, 4, 2, 1, 0, 0, 0]

    for x in range(8):
        for y in range(8 - heights[x], 8):
            sense.set_pixel(x, y, color)

def main():
    last_price = None
    last_change = None
    last_update = 0

    while True:
        current_time = time.time()

        # ⏱ Kursdaten aktualisieren
        if current_time - last_update > UPDATE_INTERVAL or last_price is None:
            try:
                last_price, last_change = get_stock_data(TICKER)
                last_update = current_time
            except Exception as e:
                sense.show_message("Fehler", text_colour=[255, 0, 0])
                print(e)
                time.sleep(10)
                continue

        # 📊 Chart anzeigen
        draw_chart(upward=(last_change >= 0))

        # 💬 Preistext wiederholt scrollen bis zum nächsten Update
        while time.time() - last_update < UPDATE_INTERVAL:
            scroll_price_message(last_price, TICKER)
            draw_chart(upward=(last_change >= 0))  # Optional: Chart nach jedem Scroll neu zeigen
            time.sleep(3.5)


main()
