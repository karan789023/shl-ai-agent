import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "shl_product_catalog.json"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "shl_product_catalog_fixed.json"

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("Original size:", len(text))


# -------------------------------------------------
# 1. Fix multiline names
# Example:
# "name": "Microsoft
# 365 (New)"
# ->
# "name": "Microsoft 365 (New)"
# -------------------------------------------------

pattern = r'("name"\s*:\s*")([^"]*?)\n([^"]*?)(")'
text = re.sub(
    pattern,
    lambda m: m.group(1) + m.group(2).strip() + " " + m.group(3).strip() + m.group(4),
    text,
    flags=re.MULTILINE,
)

# -------------------------------------------------
# 2. Convert markdown links to plain URL
# [https://abc.com](https://abc.com)
# ->
# https://abc.com
# -------------------------------------------------

text = re.sub(
    r'\[(https?://.*?)\]\((https?://.*?)\)',
    r"\2",
    text,
)

# -------------------------------------------------
# 3. Remove invalid control characters
# -------------------------------------------------

text = re.sub(
    r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
    "",
    text,
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed file written to:")
print(OUTPUT_FILE)