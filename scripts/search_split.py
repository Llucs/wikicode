"""Split the unified search index into per-language indexes and rewire the
built HTML so each language only searches its own pages.

mkdocs-material's search worker fetches `search/search_index.json` relative
to the `base` url embedded in the page config. mkdocs-static-i18n builds a
single index at the site root that mixes every language, and translated pages
still resolve `base` to the site root, so every page searches the whole site.
"""

import json
import os
import re

from mkdocs.plugins import event_priority

DEFAULT_LANG = "en"
LANGUAGES = ["en", "pt", "es", "fr", "de", "ja", "zh"]

CJK_SEPARATOR = (
    r"[\s\-\u3000\u3001\u3002\uff0c\uff0e]+"
    r"|(?<=[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f])(?=[a-zA-Z0-9])"
    r"|(?<=[a-zA-Z0-9])(?=[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f])"
)

LANG_PREFIXES = tuple(f"{lang}/" for lang in LANGUAGES if lang != DEFAULT_LANG)

BASE_RE = re.compile(r'("base"\s*:\s*")([^"]*)"')


def _split_docs(docs):
    per_lang = {lang: [] for lang in LANGUAGES if lang != DEFAULT_LANG}
    default = []
    for doc in docs:
        location = doc["location"]
        for lang, prefix in zip(per_lang, LANG_PREFIXES):
            if location.startswith(prefix):
                stripped = json.loads(json.dumps(doc))
                stripped["location"] = location[len(prefix):]
                per_lang[lang].append(stripped)
                break
        else:
            default.append(doc)
    return per_lang, default


def _rewrite_base(html, relpath):
    dirname = os.path.dirname(relpath)
    depth = 0 if not dirname else len(dirname.split("/"))
    base = "." if depth == 0 else "../" * depth

    def _replace(match):
        return match.group(1) + base + '"'

    return BASE_RE.sub(_replace, html, count=1)


@event_priority(-100)
def on_post_build(config, **kwargs):
    site_dir = config["site_dir"]
    index_path = os.path.join(site_dir, "search", "search_index.json")

    if not os.path.exists(index_path):
        return

    with open(index_path, encoding="utf-8") as f:
        data = json.load(f)

    per_lang, default = _split_docs(data["docs"])

    for lang, docs in per_lang.items():
        if not docs:
            continue
        lang_config = json.loads(json.dumps(data["config"]))
        lang_config["lang"] = [lang]
        if lang in ("ja", "zh"):
            lang_config["separator"] = CJK_SEPARATOR
        lang_dir = os.path.join(site_dir, lang, "search")
        os.makedirs(lang_dir, exist_ok=True)
        with open(os.path.join(lang_dir, "search_index.json"), "w", encoding="utf-8") as f:
            json.dump({"config": lang_config, "docs": docs}, f, ensure_ascii=False)

    default_config = json.loads(json.dumps(data["config"]))
    default_config["lang"] = [DEFAULT_LANG]
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"config": default_config, "docs": default}, f, ensure_ascii=False)

    for lang in per_lang:
        lang_root = os.path.join(site_dir, lang)
        if not os.path.isdir(lang_root):
            continue
        for dirpath, dirnames, filenames in os.walk(lang_root):
            for filename in filenames:
                if not filename.endswith(".html"):
                    continue
                html_path = os.path.join(dirpath, filename)
                with open(html_path, encoding="utf-8") as f:
                    html = f.read()
                relpath = os.path.relpath(html_path, lang_root)
                new_html = _rewrite_base(html, relpath)
                if new_html != html:
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(new_html)
