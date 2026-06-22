import os
from datetime import datetime

SECTIONS_DIR = "sections"
OUTPUT_FILE = "README.md"
ORDER = [
    "hero.md",
    "about.md",
    "focus.md",
    "techstack.md",
    "projects.md",
    "whatibuild.md",
    "stats.md",
    "snake.md",
    "philosophy.md",
    "footer.md",
]

def generate_readme():
    parts = []
    for fname in ORDER:
        fpath = os.path.join(SECTIONS_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                parts.append(f.read().strip())
    full = "\n\n".join(parts)
    full += f"\n\n---\n\n<sub>🔄 آخرین بروزرسانی خودکار: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</sub>\n"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(full)
    print("✅ README نهایی شد!")

if __name__ == "__main__":
    generate_readme()