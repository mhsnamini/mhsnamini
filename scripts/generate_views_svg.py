import json
import os
from datetime import datetime, timezone
import requests

HISTORY_FILE = "assets/view_history.json"
OUTPUT_SVG = "assets/profile-views.svg"
USERNAME = "mhsnamini"
API_URL = f"https://api.komarev.com/ghpvc?username={USERNAME}"

def fetch_current_count():
    try:
        resp = requests.get(API_URL, timeout=10)
        data = resp.json()
        return data.get("count", 0)
    except Exception:
        return None

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_sparkline_svg(history):
    if not history:
        return "<svg></svg>"
    
    counts = [point["count"] for point in history]
    min_val, max_val = min(counts), max(counts)
    width, height = 300, 60
    pad = 10
    n = len(counts)
    
    if max_val == min_val:
        # جلوگیری از تقسیم بر صفر
        max_val += 1
    
    points = []
    for i, c in enumerate(counts):
        x = pad + (width - 2*pad) * i / (n-1) if n > 1 else width/2
        y = height - pad - (c - min_val) / (max_val - min_val) * (height - 2*pad)
        points.append(f"{x:.1f},{y:.1f}")
    
    polyline = " ".join(points)
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="#0D1117" rx="8" />
  <polyline fill="none" stroke="url(#goldGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points="{polyline}" />
  <!-- دایره آخرین نقطه -->
  <circle cx="{points[-1].split(',')[0]}" cy="{points[-1].split(',')[1]}" r="3" fill="#FFD700" />
  <!-- نمایش آخرین عدد -->
  <text x="{width-10}" y="15" text-anchor="end" fill="#FFD700" font-family="monospace" font-size="12" font-weight="bold">{counts[-1]}</text>
</svg>'''
    return svg

def main():
    # ۱. گرفتن بازدید فعلی
    current_count = fetch_current_count()
    if current_count is None:
        print("⚠️ نتونستم بازدید رو بگیرم، شاید اینترنت نیست.")
        return
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # ۲. لود تاریخچه و اضافه کردن رکورد امروز
    history = load_history()
    if not history or history[-1]["date"] != today:
        history.append({"date": today, "count": current_count})
        # نگه‌داری فقط ۳۰ روز اخیر
        history = history[-30:]
        save_history(history)
    
    # ۳. تولید SVG
    svg = generate_sparkline_svg(history)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"✅ نمودار بازدید با {len(history)} روز آپدیت شد.")

if __name__ == "__main__":
    main()