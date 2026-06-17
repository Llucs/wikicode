"""Batch-translate all existing WikiCode content to configured languages."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
import concurrent.futures
from lib import (
    WORKSPACE, LANGUAGES, log,
    translate_content,
)

CONTENT_DIRS = [
    WORKSPACE / "docs",
    WORKSPACE / "projects",
    WORKSPACE / "snippets",
]

EXCLUDE_PREFIXES = [
    "docs/reports/",
]

LANGS = {l[0] for l in LANGUAGES}

def is_primary(path):
    """True if this is a primary content file (not a translation, not operational)."""
    rel = path.relative_to(WORKSPACE).as_posix()
    for prefix in EXCLUDE_PREFIXES:
        if rel.startswith(prefix):
            return False
    stem_parts = path.stem.split(".")
    if len(stem_parts) > 1 and stem_parts[-1] in LANGS:
        return False
    return (
        path.suffix == ".md"
        and not path.name.endswith("README.md")
        and not rel.startswith("memory/")
        and not rel.startswith("tasks/")
        and path.name != "LICENSE"
    )

def ensure_en(path):
    if path.name.endswith(".en.md"):
        return path
    en_path = path.with_name(path.stem + ".en.md")
    if en_path.exists():
        path.unlink()
        return en_path
    path.rename(en_path)
    log(f"Renamed: {path.relative_to(WORKSPACE)} -> {en_path.relative_to(WORKSPACE)}")
    return en_path

def translate_file(en_path):
    rel = en_path.relative_to(WORKSPACE)
    content = en_path.read_text(encoding="utf-8")
    created = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for locale, native, english_name in LANGUAGES:
            stem_base = en_path.stem.replace(".en", "")
            tx_path = en_path.with_name(stem_base + f".{locale}.md")
            if tx_path.exists():
                continue
            future = executor.submit(translate_content, content, english_name)
            futures[future] = (tx_path, locale)
        for future in concurrent.futures.as_completed(futures):
            tx_path, locale = futures[future]
            try:
                translated = future.result()
                tx_path.write_text(translated, encoding="utf-8")
                created.append(tx_path)
                log(f"Translated {rel} -> {locale}")
            except Exception as e:
                log(f"Failed to translate {rel} to {locale}: {e}")
    return created

def main():
    all_files = []
    for d in CONTENT_DIRS:
        if d.exists():
            all_files.extend(d.rglob("*.md"))

    content_files = [f for f in all_files if is_primary(f)]
    content_files.sort()

    log(f"Found {len(content_files)} primary content files")

    for path in content_files:
        en_path = ensure_en(path)
        translate_file(en_path)

    log("Batch translation complete!")

if __name__ == "__main__":
    main()
