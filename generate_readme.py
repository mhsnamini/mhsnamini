import os
from datetime import datetime

SECTIONS_DIR = "sections"
OUTPUT_FILE = "README.md"
# ترتیب دلخواه فایل‌ها
ORDER = [
    "header.md",
    "intro.md",
    "about.md",
    "focus.md",
    "techstack.md",
    "projects.md",
    "whatibuild.md",
    "stats.md",
    "philosophy.md",
    "connect.md",
]

def generate_readme():
    content_parts = []
    for filename in ORDER:
        filepath = os.path.join(SECTIONS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content_parts.append(f.read().strip())
        else:
            print(f"⚠️ فایل {filename} پیدا نشد، رد شد.")
    
    full_content = "\n\n".join(content_parts)
    # می‌تونی آخرش یه تایم‌استمپ اتوماتیک هم بذاری
    full_content += f"\n\n---\n\n<sub>🔄 آخرین به‌روزرسانی خودکار: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</sub>\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(full_content)
    print("✅ README.md با موفقیت ساخته شد.")

if __name__ == "__main__":
    generate_readme()