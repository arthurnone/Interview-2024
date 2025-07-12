import glob
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

# 1. Find your candles JSON file
files = glob.glob("./output/*_candles.json")
if not files:
    raise FileNotFoundError(
        "No candles JSON file found in the working directory.")
candles_filename = files[0]

# 2. Load the JSON
with open(candles_filename, 'r', encoding='utf-8') as f:
    raw_candles = json.load(f)

# 3. Parse into lists
times = [datetime.fromisoformat(c['minute']) for c in raw_candles]
opens = [c['open'] for c in raw_candles]
highs = [c['high'] for c in raw_candles]
lows = [c['low'] for c in raw_candles]
closes = [c['close'] for c in raw_candles]

# 4. Convert to matplotlib date numbers
dates = mdates.date2num(times)
width = (1/24/60) * 0.8  # width = 1 minute (in days) × 0.8

# 5. Plot
fig, ax = plt.subplots(figsize=(12, 6))

for dt, o, h, l, c in zip(dates, opens, highs, lows, closes):
    # high–low line
    ax.vlines(dt, l, h)
    # open–close box
    rect = Rectangle(
        (dt - width/2, min(o, c)),
        width,
        abs(c - o)
    )
    ax.add_patch(rect)

# 6. Beautify
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel("Time (HH:MM)")
plt.ylabel("Price (JPY)")
plt.title("BTC/JPY 1-Minute Candlestick Chart")
plt.gcf().autofmt_xdate()
plt.tight_layout()

# 7. Save as PNG
image_filename = candles_filename.replace(".json", ".png")
plt.savefig(image_filename)
print(f"Saved candlestick chart to {image_filename}")
