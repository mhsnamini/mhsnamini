import json
import os
import re
from datetime import datetime, timezone
import requests

HISTORY_FILE = "assets/view_history.json"
OUTPUT_SVG = "assets/profile-views.svg"
USERNAME = "mhsnamini"

# این API یک SVG برمی‌گردونه که توش تعداد بازدید هست
API_URL = f"https://visitor-badge.laobi.icu/badge?page_id={USERNAME}.{USERNAME}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_current_count():
    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=10)
        # SVG برگشتی شامل یه تگ text با عدده
        # مثال: <text x="..." y="..." ...>123</text>
        match = re.search(r'>(\d+)<', resp.text)
        if match:
            return int(match.group(1))
        else:
            print("❌ نتونستم عدد رو از SVG بکشم، پاسخ:", resp.text[:200])
            return None
    except Exception as e:
        print(f"❌ خطا در گرفتن بازدید: {e}")
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
  <circle cx="{points[-1].split(',')[0]}" cy="{points[-1].split(',')[1]}" r="3" fill="#FFD700" />
  <text x="{width-10}" y="15" text-anchor="end" fill="#FFD700" font-family="monospace" font-size="12" font-weight="bold">{counts[-1]}</text>
</svg>'''
    return svg

def main():
    current_count = fetch_current_count()
    if current_count is None:
        print("⚠️ نتونستم بازدید رو بگیرم، مطمئن شو اینترنت وصله و API در دسترسه.")
        return
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    history = load_history()
    if not history or history[-1]["date"] != today:
        history.append({"date": today, "count": current_count})
        history = history[-30:]
        save_history(history)
    else:
        # آپدیت عدد امروز
        history[-1]["count"] = current_count
        save_history(history)
    
    svg = generate_sparkline_svg(history)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"✅ نمودار بازدید با {len(history)} روز آپدیت شد - آخرین بازدید: {current_count}")

if __name__ == "__main__":
    main()