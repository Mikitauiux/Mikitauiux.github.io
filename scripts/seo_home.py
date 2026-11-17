"""Injects SEO head tags into index.html and ru/index.html. Idempotent: re-run after edits."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mikitauiux.github.io"

PERSON = {
    "@type": "Person", "@id": f"{SITE}/#person",
    "name": "Mikita Yurkevich", "alternateName": ["Микита Юркевич", "mikitauiux"],
    "jobTitle": "Senior Product Designer", "url": f"{SITE}/", "image": f"{SITE}/assets/mikita.jpg",
    "email": "mailto:mikitauiux@gmail.com",
    "address": {"@type": "PostalAddress", "addressLocality": "Wroclaw", "addressCountry": "PL"},
    "knowsAbout": ["Product Design", "UI/UX Design", "UX Research", "Design Systems", "Conversion Rate Optimization", "iGaming", "SaaS", "Figma"],
    "sameAs": ["https://www.linkedin.com/in/mikitauiux", "https://www.behance.net/mikitayurkevich", "https://t.me/Burysta"],
}

PAGES = {
    "index.html": dict(lang="en", locale="en_US", alt_locale="ru_RU", url=f"{SITE}/",
        title="Mikita Yurkevich — Senior Product Designer · UI/UX for iGaming &amp; SaaS",
        desc="Mikita Yurkevich, Senior Product Designer in Wroclaw. UI/UX for iGaming and SaaS: conversion-focused UX, complex interfaces, design systems. Case studies inside."),
    "ru/index.html": dict(lang="ru", locale="ru_RU", alt_locale="en_US", url=f"{SITE}/ru/",
        title="Микита Юркевич (Mikita Yurkevich) — Senior Product Designer, UI/UX дизайнер",
        desc="Микита Юркевич — Senior Product / UI/UX дизайнер из Вроцлава. iGaming и SaaS: конверсионный UX, сложные интерфейсы, дизайн-системы. Кейсы bookmaker.XYZ и Caswino."),
}

START, END = "<!-- seo -->", "<!-- /seo -->"

def block(p):
    up = "../" if p["lang"] == "ru" else ""
    ld = {"@context": "https://schema.org", "@graph": [PERSON, {
        "@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Mikita Yurkevich — Portfolio",
        "inLanguage": ["en", "ru"], "author": {"@id": f"{SITE}/#person"}},
        {"@type": "ProfilePage", "url": p["url"], "name": p["title"].replace("&amp;", "&"), "inLanguage": p["lang"],
         "mainEntity": {"@id": f"{SITE}/#person"}, "isPartOf": {"@id": f"{SITE}/#website"}}]}
    return f"""  {START}
  <link rel="canonical" href="{p["url"]}" />
  <link rel="alternate" hreflang="en" href="{SITE}/" />
  <link rel="alternate" hreflang="ru" href="{SITE}/ru/" />
  <link rel="alternate" hreflang="x-default" href="{SITE}/" />
  <meta name="google-site-verification" content="p7FCl4aFB9ftGhCtMuLh3U7LVQe6HWwck-kR8G2EBNY" />
  <meta name="author" content="Mikita Yurkevich" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0a0a0b" />
  <link rel="icon" href="{up}favicon.ico" sizes="any" />
  <link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="{up}apple-touch-icon.png" />
  <meta property="og:type" content="profile" />
  <meta property="og:site_name" content="Mikita Yurkevich" />
  <meta property="og:title" content="{p["title"]}" />
  <meta property="og:description" content="{p["desc"]}" />
  <meta property="og:url" content="{p["url"]}" />
  <meta property="og:image" content="{SITE}/assets/og.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="{p["locale"]}" />
  <meta property="og:locale:alternate" content="{p["alt_locale"]}" />
  <meta property="profile:first_name" content="Mikita" />
  <meta property="profile:last_name" content="Yurkevich" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{p["title"]}" />
  <meta name="twitter:description" content="{p["desc"]}" />
  <meta name="twitter:image" content="{SITE}/assets/og.jpg" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  {END}
"""

for rel, p in PAGES.items():
    f = ROOT / rel
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{p["desc"]}" />', s, count=1)
    s = re.sub(r'\s*<link rel="alternate" hreflang="[a-z-]+" href="[^"]*" />', "", s)  # moved into the block
    s = re.sub(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, flags=re.S)
    s = re.sub(r'^[ \t]*<meta name="description"', '  <meta name="description"', s, count=1, flags=re.M)
    s = s.replace('  <meta name="description"', block(p) + '  <meta name="description"', 1)
    f.write_text(s, encoding="utf-8")
    print("updated", rel)
