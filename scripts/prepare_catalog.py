import json
import re
from pathlib import Path

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "shl_product_catalog_fixed.json"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "catalog.json"

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def generate_slug(name: str) -> str:
    """
    Convert assessment name into URL friendly slug.
    """
    if not name:
        return ""

    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)

    return slug.strip("-")


def generate_keywords(item):
    """
    Merge useful searchable keywords.
    """

    keywords = set()

    keywords.update(item.get("keys", []))
    keywords.update(item.get("job_levels", []))
    keywords.update(item.get("languages", []))

    return sorted(list(keywords))


def build_search_text(item):
    """
    Build one searchable text block.
    """

    parts = []

    parts.append(item.get("name", ""))

    parts.append(item.get("description", ""))

    parts.extend(item.get("keys", []))

    parts.extend(item.get("job_levels", []))

    parts.extend(item.get("languages", []))

    return " ".join(str(x) for x in parts if x)


def calculate_quality(item):
    """
    Simple quality score.
    """

    score = 0

    if item.get("name"):
        score += 20

    if item.get("description"):
        score += 20

    if item.get("keys"):
        score += 20

    if item.get("job_levels"):
        score += 20

    if item.get("link"):
        score += 20

    return score


def clean_text(text):
    """
    Remove unnecessary whitespace.
    """

    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# LOAD RAW JSON
# =====================================================

print("Loading SHL Catalog...")

with open(RAW_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

print(f"Loaded {len(raw_data)} assessments")

# =====================================================
# PROCESS
# =====================================================

catalog = []

seen_urls = set()

for item in raw_data:

    name = clean_text(item.get("name", ""))

    url = clean_text(item.get("link", ""))

    description = clean_text(item.get("description", ""))

    if not name:
        continue

    if not url:
        continue

    if url in seen_urls:
        continue

    seen_urls.add(url)

    slug = generate_slug(name)

    keywords = generate_keywords(item)

    search_text = build_search_text(item)

    quality = calculate_quality(item)

    assessment = {

        "id": item.get("entity_id"),

        "name": name,

        "slug": slug,

        "url": url,

        "description": description,

        "summary": description[:250],

        "skills": item.get("keys", []),

        "keywords": keywords,

        "search_text": search_text,

        # Future embeddings
        "embedding_text": search_text,

        "quality_score": quality,

        "job_levels": item.get("job_levels", []),

        "languages": item.get("languages", []),

        "duration": item.get("duration", ""),

        "remote": str(item.get("remote", "")).lower() == "yes",

        "adaptive": str(item.get("adaptive", "")).lower() == "yes",

        "status": item.get("status", "")
    }

    catalog.append(assessment)

# =====================================================
# SAVE
# =====================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

print("=" * 60)
print("Knowledge Base Generated Successfully")
print("=" * 60)
print(f"Total Assessments : {len(catalog)}")
print(f"Saved File        : {OUTPUT_FILE}")
print("=" * 60)