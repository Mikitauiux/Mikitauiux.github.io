"""Builds the case study pages in English (site root) and Russian (/ru/).

Edit the texts below, then run from the repo root:
    python scripts/build_cases.py
Needs Pillow (pip install pillow) to read slide sizes.
"""
import html
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mikitauiux.github.io"
V = "8"  # bump when styles.css / main.js change so browsers drop cached copies

UI = {
    "en": dict(
        nav=[("index.html#work", "Work"), ("index.html#impact", "Impact"), ("index.html#experience", "Experience")],
        contact="Contact", status="Open to work", back="← All work", case="Case", next="(Next case)",
        cursor_next="Next", contact_label="(Contact) — Got a product that should convert better?",
        talk=("Let's", "talk"), city="Wroclaw", case_study="Case study", cover="cover animation",
        mail="Email", figma="Open in Figma ↗", cv="CV ↗",
        desc="Case study by Mikita Yurkevich, Senior Product Designer.",
    ),
    "ru": dict(
        nav=[("index.html#work", "Работы"), ("index.html#impact", "Результаты"), ("index.html#experience", "Опыт")],
        contact="Контакты", status="Открыт к работе", back="← Все работы", case="Кейс", next="(Следующий кейс)",
        cursor_next="Далее", contact_label="(Контакты) — Есть продукт, который должен конвертить лучше?",
        talk=("Пиши", "мне"), city="Вроцлав", case_study="Кейс", cover="анимация обложки",
        mail="Почта", figma="Открыть в Figma ↗", cv="Резюме ↗",
        desc="Кейс Микиты Юркевича, Senior Product Designer.",
    ),
}

CASES = [
    dict(
        slug="bookmaker", figma="https://www.figma.com/design/nvbJLIjJWQu5SkyyD2rKoX?node-id=6-2", idx="01", accent="#b7a6ff", year="2025", title="bookmaker.XYZ",
        stats=[("+", "700", "%"), ("+", "400", "%"), ("", "4", "")],
        shots=["03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"],
        en=dict(
            tagline="Web3 casino & sportsbook. Onboarding funnel redesign",
            lead="bookmaker.XYZ is a Web3 casino and sportsbook: players connect a wallet or a social account, fund in USDT and bet on sports, e-sports and casino games. I redesigned the first-session journey — from the first visit to the first deposit.",
            meta=[("Role", "Product Designer — research, UX, UI"), ("Product", "Web3 casino & sportsbook"),
                  ("Platforms", "Web · Mobile web"), ("Scope", "Onboarding funnel, promotions, bonuses, profile")],
            stat_labels=["Conversion to sign-up", "First-time deposits (FTD)", "Funnel changes shipped"],
            alts=["Problem: a generic onboarding lost players at every step",
                  "Four bets on the funnel: segment from the first click, create urgency, keep the momentum, catch the ones who leave",
                  "Onboarding flow prototype", "Casino or sport — the player picks a welcome offer",
                  "Each segment lands on its own lobby", "Deposit flow prototype",
                  "Deposit opens right after sign-up with the chosen bonus pre-applied",
                  "No deposit? A soft opt-in keeps the bonus and brings the player back",
                  "Results: +700% conversion to sign-up, +400% first-time deposits",
                  "Promotions, bonuses and tournaments", "Mobile-first screens for Web3 players",
                  "Visual language: colours and typography"],
        ),
        ru=dict(
            tagline="Web3-казино и спортбеттинг. Редизайн воронки онбординга",
            lead="bookmaker.XYZ — Web3-казино и спортбеттинг: игроки подключают кошелёк или соцсеть, пополняют баланс в USDT и ставят на спорт, киберспорт и казино. Я перепроектировал первую сессию — от первого визита до первого депозита.",
            meta=[("Роль", "Product Designer — исследование, UX, UI"), ("Продукт", "Web3-казино и спортбеттинг"),
                  ("Платформы", "Веб · Мобильный веб"), ("Задачи", "Воронка онбординга, промо, бонусы, профиль")],
            stat_labels=["Конверсия в регистрацию", "Первые депозиты (FTD)", "Изменения воронки в продакшене"],
            alts=["Проблема: общий онбординг терял игроков на каждом шаге",
                  "Четыре гипотезы для воронки: сегмент с первого клика, срочность, сохранить темп, вернуть ушедших",
                  "Прототип онбординга", "Казино или спорт — игрок выбирает приветственный бонус",
                  "Каждый сегмент попадает в своё лобби", "Прототип депозита",
                  "Депозит открывается сразу после регистрации с выбранным бонусом",
                  "Нет депозита? Мягкая подписка сохраняет бонус и возвращает игрока",
                  "Результаты: +700% к конверсии в регистрацию, +400% к первым депозитам",
                  "Промо, бонусы и турниры", "Мобильные экраны для Web3-игроков",
                  "Визуальный язык: цвета и типографика"],
        ),
    ),
    dict(
        slug="caswino", figma="https://www.figma.com/design/nvbJLIjJWQu5SkyyD2rKoX?node-id=0-1", idx="02", accent="#ffc700", year="2023", title="Caswino",
        stats=[("", "80", "+"), ("", "85", "+"), ("", "3", "")],
        shots=["03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
        en=dict(
            tagline="Crypto casino platform. UX/UI design",
            lead="Caswino is a crypto-first online casino with thousands of slots, live tables and instant games. The goal of the redesign was to make the product feel premium and fast: find a game in seconds, top up in a couple of taps and always see which bonuses are waiting.",
            meta=[("Role", "Product Designer (UX/UI)"), ("Platforms", "Desktop · Tablet · Mobile web"),
                  ("Scope", "UX flows, UI design, design system, prototypes"), ("Industry", "iGaming · Crypto casino")],
            stat_labels=["Desktop screens", "Mobile screens", "Breakpoints: 1440 / 1024 / 375"],
            alts=["Challenges and goals: find a game fast, simple crypto payments, keep players engaged",
                  "Product walkthrough prototype", "Home and lobby with welcome offer, category tabs and game rails",
                  "Game experience: game page, quick-deposit bar and split-screen mode",
                  "Wallet and crypto payments: multi-currency deposit, withdrawal and exchange",
                  "Player account: dashboard, bonuses catalogue and bet history",
                  "Sign up and log in with social login and clear validation", "Mobile experience prototype",
                  "Tablet layout at 1024", "Visual language: colours and typography"],
        ),
        ru=dict(
            tagline="Крипто-казино. UX/UI-дизайн",
            lead="Caswino — крипто-казино с тысячами слотов, лайв-столами и быстрыми играми. Цель редизайна — сделать продукт премиальным и быстрым: найти игру за секунды, пополнить баланс в пару тапов и всегда видеть, какие бонусы ждут.",
            meta=[("Роль", "Product Designer (UX/UI)"), ("Платформы", "Десктоп · Планшет · Мобильный веб"),
                  ("Задачи", "UX-сценарии, UI-дизайн, дизайн-система, прототипы"), ("Индустрия", "iGaming · Крипто-казино")],
            stat_labels=["Экранов для десктопа", "Экранов для мобайла", "Брейкпоинта: 1440 / 1024 / 375"],
            alts=["Задачи и цели: быстро найти игру, простые крипто-платежи, удержание игроков",
                  "Прототип продукта", "Главная и лобби: приветственный бонус, категории и подборки игр",
                  "Игровой экран: страница игры, быстрый депозит и режим нескольких игр",
                  "Кошелёк и крипто-платежи: мультивалютный депозит, вывод и обмен",
                  "Личный кабинет: дашборд, каталог бонусов и история ставок",
                  "Регистрация и вход: соцсети и понятная валидация", "Прототип мобильной версии",
                  "Планшетная версия 1024", "Визуальный язык: цвета и типографика"],
        ),
    ),
    dict(
        slug="backoffice", figma="https://www.figma.com/design/nvbJLIjJWQu5SkyyD2rKoX?node-id=12-2", idx="03", accent="#8a87ff", year="2025", title="Casino Back-office",
        stats=[("", "4", ""), ("", "90", "+"), ("", "6", "")],
        shots=["03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"],
        en=dict(
            tagline="Crypto casino admin panel on Strapi. Back-office UX/UI",
            lead="A custom admin panel built on top of Strapi for a crypto casino. Operators launch bonus campaigns, moderate payouts, manage players and curate the game lobby — without asking developers. Each of the four modules was designed around one concrete job of one team.",
            meta=[("Role", "Product Designer — UX, UI, design system"), ("Product", "Casino back-office on Strapi"),
                  ("Users", "CRM, payments & risk, support, content"), ("Scope", "Bonus engine, payouts, players, game lobby")],
            stat_labels=["Product modules", "Screens & states designed", "Reusable CRM building blocks"],
            alts=["Four roles, four jobs: CRM manager, payments & risk, support and content manager",
                  "Information architecture grouped by the team that uses it",
                  "Flow: building a bonus campaign from reusable blocks",
                  "Five blocks, one campaign: config, offer, trigger and segment",
                  "A 4-step campaign wizard with a live audience estimate",
                  "Flow: moderating a withdrawal request",
                  "One screen to decide: wager progress, limits, GGR and history in one modal",
                  "Player 360 for support: user list, profile, wallet and account status",
                  "Curating the game lobby: collections, games and group icons",
                  "Impact: 0 developer tickets to launch a bonus, 4 steps to a live campaign, 1 screen per payout decision",
                  "Built on Strapi Design System: colour tokens, foundations and components"],
        ),
        ru=dict(
            tagline="Админка крипто-казино на Strapi. UX/UI бэк-офиса",
            lead="Кастомная админ-панель на базе Strapi для крипто-казино. Операторы запускают бонусные кампании, модерируют выплаты, управляют игроками и собирают лобби игр — без помощи разработчиков. Каждый из четырёх модулей спроектирован вокруг одной конкретной задачи одной команды.",
            meta=[("Роль", "Product Designer — UX, UI, дизайн-система"), ("Продукт", "Бэк-офис казино на Strapi"),
                  ("Пользователи", "CRM, платежи и риски, саппорт, контент"), ("Задачи", "Бонусный движок, выплаты, игроки, лобби игр")],
            stat_labels=["Модуля продукта", "Экранов и состояний", "Переиспользуемых блоков CRM"],
            alts=["Четыре роли — четыре задачи: CRM-менеджер, платежи и риски, саппорт, контент-менеджер",
                  "Информационная архитектура сгруппирована по командам",
                  "Сценарий: сборка бонусной кампании из готовых блоков",
                  "Пять блоков — одна кампания: конфиг, оффер, триггер, сегмент",
                  "Мастер создания кампании в 4 шага с живой оценкой аудитории",
                  "Сценарий: модерация заявки на вывод",
                  "Решение на одном экране: прогресс вейджера, лимиты, GGR и история в одном окне",
                  "Player 360 для саппорта: список игроков, профиль, кошелёк и статус аккаунта",
                  "Управление лобби: коллекции, добавление игр и иконки групп",
                  "Результат: 0 тикетов разработчикам на запуск бонуса, 4 шага до кампании, 1 экран на решение по выплате",
                  "На базе Strapi Design System: цветовые токены, основы и компоненты"],
        ),
    ),
    dict(
        slug="knucklebonz", idx="04", accent="#ff4a3d", year="2026", title="KnuckleBonz",
        stats=[("", "3", ""), ("", "4", ""), ("", "25", "+")],
        shots=["03", "04", "05", "06", "07", "08", "09", "10", "11"],
        en=dict(
            tagline="Rock & metal metaverse. Game UI for desktop, mobile and Telegram",
            lead="KnuckleBonz makes collectible statues of rock and metal legends. This project turns the brand into a playable world: a 3D city where fans explore locations, dress their avatar in band merch, play music mini-games and collect 3D vinyls — plus a Telegram mini-game that brings new players in.",
            meta=[("Role", "UI/UX Designer — game UI & flows"), ("Platforms", "Desktop · Mobile landscape · Telegram"),
                  ("Scope", "Onboarding, map, avatar, shop, mini-games, collection, social"), ("Genre", "Music metaverse · casual games")],
            stat_labels=["Platforms", "Mini-games designed", "Game areas & flows"],
            alts=["Core loop: explore the city, customise the avatar, play mini-games, earn notes",
                  "The city is the menu: a 3D map with location cards and the player profile",
                  "Log in with the store account: one KnuckleBonz account for the shop and the game",
                  "Avatar editor and merch shop with a live 3D preview",
                  "Music mini-games: Can Toss, Trivia, Treasure Hunt and CrowdSurf",
                  "Collect 3D vinyls of legendary albums",
                  "Telegram mini-app: a quick runner that brings new players into the world",
                  "Mobile landscape: compact side menu and touch-sized location cards",
                  "Visual language: colours and typography"],
        ),
        ru=dict(
            tagline="Рок- и метал-метавселенная. Игровой UI для десктопа, мобайла и Telegram",
            lead="KnuckleBonz делает коллекционные статуэтки легенд рока и метала. Проект превращает бренд в игровой мир: 3D-город, где фанаты исследуют локации, одевают аватара в мерч групп, играют в музыкальные мини-игры и собирают 3D-винилы, — плюс мини-игра в Telegram, которая приводит новых игроков.",
            meta=[("Роль", "UI/UX Designer — игровой UI и сценарии"), ("Платформы", "Десктоп · Мобайл (landscape) · Telegram"),
                  ("Задачи", "Онбординг, карта, аватар, магазин, мини-игры, коллекция, соцфункции"), ("Жанр", "Музыкальная метавселенная · казуальные игры")],
            stat_labels=["Платформы", "Мини-игры", "Игровых зон и сценариев"],
            alts=["Игровой цикл: исследуй город, настрой аватара, играй в мини-игры, зарабатывай ноты",
                  "Город — это меню: 3D-карта с карточками локаций и профиль игрока",
                  "Вход через аккаунт магазина: один аккаунт KnuckleBonz для магазина и игры",
                  "Редактор аватара и магазин мерча с живым 3D-превью",
                  "Музыкальные мини-игры: Can Toss, Trivia, Treasure Hunt и CrowdSurf",
                  "Коллекция 3D-винилов легендарных альбомов",
                  "Мини-приложение в Telegram: быстрый раннер, который приводит новых игроков",
                  "Мобильная landscape-версия: компактное меню и крупные карточки локаций",
                  "Визуальный язык: цвета и типографика"],
        ),
    ),
    dict(
        slug="drive-storage", idx="05", accent="#ff3d6e", year="2026", title="Drive Storage",
        stats=[("", "0", " PLN"), ("", "11", ""), ("", "2", "")],
        shots=["03", "04", "05", "06", "07", "08", "09", "10"],
        en=dict(
            tagline="“Try for Free” landing page and explainer video storyboard",
            lead="Drive Storage rents self-storage units in Poland. Renting storage unseen feels risky, and a visit with a salesperson feels like pressure. The “Try for Free” offer lets anyone book a free, self-guided visit to see a unit before renting. I designed the landing page that sells this offer and the explainer video that shows how it works.",
            meta=[("Role", "UI/UX Designer — landing & motion"), ("Deliverables", "Landing page · explainer storyboard"),
                  ("Platforms", "Desktop · Mobile"), ("Languages", "English · Polish")],
            stat_labels=["Cost of the visit", "Scenes in the explainer", "Languages: EN & PL"],
            alts=["Answer every doubt before it appears: no salesperson, no card, any time, access by phone",
                  "User journey from click to gate: online booking, then a visit in person",
                  "The landing page: promise, how it works, real product UI, guarantees, FAQ and final CTA",
                  "“This is exactly what you’ll see”: real screens from the booking flow",
                  "Booking flow: choose your space",
                  "Explainer storyboard: 11 scenes, about 40 seconds, 16:9",
                  "Mobile layouts in English and Polish",
                  "Visual language: colours and typography"],
        ),
        ru=dict(
            tagline="Лендинг «Try for Free» и сториборд видео-эксплейнера",
            lead="Drive Storage сдаёт в аренду складские боксы в Польше. Арендовать бокс не глядя — рискованно, а визит с менеджером ощущается как давление. Оффер «Try for Free» позволяет бесплатно забронировать самостоятельный визит и увидеть бокс до аренды. Я спроектировал лендинг, который продаёт этот оффер, и видео-эксплейнер о том, как всё работает.",
            meta=[("Роль", "UI/UX Designer — лендинг и моушн"), ("Результат", "Лендинг · сториборд эксплейнера"),
                  ("Платформы", "Десктоп · Мобайл"), ("Языки", "Английский · Польский")],
            stat_labels=["Стоимость визита", "Сцен в эксплейнере", "Языка: EN и PL"],
            alts=["Снять все сомнения заранее: без менеджера, без карты, в любое время, доступ по телефону",
                  "Путь пользователя от клика до ворот: бронь онлайн, затем визит на место",
                  "Лендинг: обещание, как это работает, реальный UI продукта, гарантии, FAQ и финальный CTA",
                  "«Ровно то, что вы увидите»: реальные экраны процесса бронирования",
                  "Сценарий бронирования: выбор бокса",
                  "Сториборд эксплейнера: 11 сцен, около 40 секунд, 16:9",
                  "Мобильные макеты на английском и польском",
                  "Визуальный язык: цвета и типографика"],
        ),
    ),
]


def shot(case, num, alt, up):
    e = html.escape
    folder = ROOT / "assets" / case["slug"]
    base = f'{up}assets/{case["slug"]}/{num}'
    if (folder / f"{num}.mp4").exists():
        w, h = Image.open(folder / f"{num}.jpg").size
        return (f'      <figure class="cs-shot"><video src="{base}.mp4" poster="{base}.jpg" width="{w}" height="{h}" '
                f'muted loop playsinline preload="none" data-autoplay aria-label="{e(alt)}"></video></figure>')
    w, h = Image.open(folder / f"{num}.webp").size
    return (f'      <figure class="cs-shot"><img src="{base}.webp" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="{e(alt)}" /></figure>')


def title_lines(title):
    """One masked line per word, so long titles stack instead of overflowing."""
    return "".join(f'<span class="line"><span class="split">{html.escape(w)}</span></span>' for w in title.split())

def seo_head(case, lang, title, desc, up):
    """Canonical, hreflang, icons, Open Graph and JSON-LD for one case page."""
    e = html.escape
    path = f'{"ru/" if lang == "ru" else ""}{case["slug"]}.html'
    url = f"{SITE}/{path}"
    img = f'{SITE}/assets/{case["slug"]}/01.jpg'
    w, h = Image.open(ROOT / "assets" / case["slug"] / "01.jpg").size
    home = f"{SITE}/ru/" if lang == "ru" else f"{SITE}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CreativeWork", "@id": url + "#work", "name": case["title"], "headline": title,
         "description": desc, "url": url, "image": img, "inLanguage": lang, "dateCreated": case["year"],
         "genre": "UI/UX case study",
         "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Mikita Yurkevich", "url": f"{SITE}/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mikita Yurkevich", "item": home},
            {"@type": "ListItem", "position": 2, "name": case["title"], "item": url}]}]}
    alt_locale = "en_US" if lang == "ru" else "ru_RU"
    locale = "ru_RU" if lang == "ru" else "en_US"
    return f"""  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="en" href="{SITE}/{case["slug"]}.html" />
  <link rel="alternate" hreflang="ru" href="{SITE}/ru/{case["slug"]}.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE}/{case["slug"]}.html" />
  <meta name="author" content="Mikita Yurkevich" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0a0a0b" />
  <link rel="icon" href="{up}favicon.ico" sizes="any" />
  <link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="{up}apple-touch-icon.png" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mikita Yurkevich" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{img}" />
  <meta property="og:image:width" content="{w}" />
  <meta property="og:image:height" content="{h}" />
  <meta property="og:locale" content="{locale}" />
  <meta property="og:locale:alternate" content="{alt_locale}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(desc)}" />
  <meta name="twitter:image" content="{img}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""


def page(case, nxt, lang):
    e = html.escape
    t, ui = case[lang], UI[lang]
    up = "../" if lang == "ru" else ""
    other = f'../{case["slug"]}.html' if lang == "ru" else f'ru/{case["slug"]}.html'
    en_cur, ru_cur = ('aria-current="page"', '') if lang == "en" else ('', 'aria-current="page"')
    en_href, ru_href = (f'{case["slug"]}.html', other) if lang == "en" else (other, f'{case["slug"]}.html')
    nav = "\n".join(f'      <a href="{h}" data-transition>{e(l)}</a>' for h, l in ui["nav"])
    meta = "\n".join(f'        <div data-fade><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in t["meta"])
    stats = "\n".join(
        f'        <div class="stat"><p class="stat__num" data-prefix="{p}" data-to="{n}" data-suffix="{s}">{p}{n}{s}</p>'
        f'<p class="stat__label">{e(l)}</p></div>'
        for (p, n, s), l in zip(case["stats"], t["stat_labels"]))
    shots = "\n".join(shot(case, n, a, up) for n, a in zip(case["shots"], t["alts"]))
    title = f'{case["title"]} — {t["tagline"]} | Mikita Yurkevich'
    desc = f'{t["tagline"]}. {ui["desc"]}'
    figma = (f'      <p class="cs-hero__actions" data-fade><a class="btn" href="{e(case["figma"])}" target="_blank" rel="noopener" '
             f'data-magnetic data-cursor="Figma">{e(ui["figma"])}</a></p>\n') if case.get("figma") else ""
    return f'''<!doctype html>
<!-- Generated by scripts/build_cases.py — edit texts there, not here. -->
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
{seo_head(case, lang, title, desc, up)}
  <script>document.documentElement.classList.add('js')</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Manrope:wght@400;500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{up}styles.css?v={V}" />
</head>
<body class="cs-page" style="--cs:{case["accent"]}">
  <div class="curtain" aria-hidden="true"></div>
  <div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>

  <header class="nav">
    <div class="nav__left">
      <a href="index.html" class="nav__logo" data-transition data-magnetic>MY<sup>®</sup></a>
      <span class="nav__status">{e(ui["status"])}<i aria-hidden="true"></i></span>
    </div>
    <nav class="nav__links" aria-label="Main">
{nav}
      <a href="#contact">{e(ui["contact"])}</a>
    </nav>
    <div class="nav__right">
      <a class="nav__cv" href="https://drive.google.com/file/d/1NTE3bZizyj5bP6LSe6BAsHyuyQnJgQY2/view?usp=sharing" target="_blank" rel="noopener">{e(ui["cv"])}</a>
      <div class="nav__lang" aria-label="Language"><a href="{en_href}" hreflang="en" lang="en" {en_cur} data-transition>EN</a><a href="{ru_href}" hreflang="ru" lang="ru" {ru_cur} data-transition>RU</a></div>
    </div>
  </header>

  <main>
    <section class="cs-hero">
      <a href="index.html#work" class="cs-back" data-transition data-fade>{e(ui["back"])}</a>
      <div class="cs-hero__top" data-fade><span>({e(ui["case"])} {case["idx"]})</span><span>{case["year"]}</span></div>
      <h1 class="cs-hero__title">{title_lines(case["title"])}</h1>
      <p class="cs-hero__tagline" data-fade>{e(t["tagline"])}</p>
      <p class="cs-hero__lead" data-fade>{e(t["lead"])}</p>
{figma}      <dl class="cs-meta">
{meta}
      </dl>
      <div class="stats">
{stats}
      </div>
    </section>

    <section class="cs-cover">
      <div class="cs-cover__frame">
        <video src="{up}assets/{case["slug"]}/01.mp4" poster="{up}assets/{case["slug"]}/01.jpg" muted loop playsinline preload="auto" data-autoplay aria-label="{e(case["title"])} — {e(ui["cover"])}"></video>
      </div>
    </section>

    <section class="cs-shots" aria-label="{e(ui["case_study"])}">
{shots}
    </section>

    <section class="cs-next">
      <a href="{nxt["slug"]}.html" class="cs-next__link" data-transition data-cursor="{e(ui["cursor_next"])}">
        <p class="intro__label">{e(ui["next"])}</p>
        <h2 class="cs-next__title">{title_lines(nxt["title"])}</h2>
        <p class="cs-next__tagline">{e(nxt[lang]["tagline"])} →</p>
      </a>
    </section>
  </main>

  <footer class="contact" id="contact">
    <p class="intro__label">{e(ui["contact_label"])}</p>
    <h2 class="contact__title"><span class="line"><span class="split">{e(ui["talk"][0])}</span></span><span class="line"><span class="split">{e(ui["talk"][1])}</span></span></h2>
    <div class="contact__cta">
      <a class="contact__btn" href="mailto:mikitauiux@gmail.com" data-magnetic><small>{e(ui["mail"])}</small><span>mikitauiux@gmail.com</span></a>
      <a class="contact__btn" href="https://t.me/Burysta" target="_blank" rel="noopener" data-magnetic><small>Telegram</small><span>@Burysta ↗</span></a>
    </div>
    <div class="contact__bottom">
      <ul class="contact__links">
        <li><a href="https://www.linkedin.com/in/mikitauiux" target="_blank" rel="noopener">LinkedIn ↗</a></li>
        <li><a href="https://www.behance.net/mikitayurkevich" target="_blank" rel="noopener">Behance ↗</a></li>
        <li><a href="https://drive.google.com/file/d/1NTE3bZizyj5bP6LSe6BAsHyuyQnJgQY2/view?usp=sharing" target="_blank" rel="noopener">{e(ui["cv"])}</a></li>
      </ul>
      <p>{e(ui["city"])} · <span class="clock">--:--</span></p>
      <p>© 2026 Mikita Yurkevich</p>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
  <script src="{up}main.js?v={V}"></script>
</body>
</html>
'''


for lang in ("en", "ru"):
    out_dir = ROOT if lang == "en" else ROOT / "ru"
    out_dir.mkdir(exist_ok=True)
    for i, c in enumerate(CASES):
        assert len(c["shots"]) == len(c[lang]["alts"]), (c["slug"], lang)
        (out_dir / f'{c["slug"]}.html').write_text(page(c, CASES[(i + 1) % len(CASES)], lang), encoding="utf-8")
        print("wrote", (out_dir / f'{c["slug"]}.html').relative_to(ROOT))


def sitemap():
    """sitemap.xml: home + every case, each with its EN/RU alternates."""
    pairs = [("", "ru/", "1.0")] + [(f'{c["slug"]}.html', f'ru/{c["slug"]}.html', "0.8") for c in CASES]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for en, ru, pr in pairs:
        for loc in (en, ru):
            out += ["  <url>", f"    <loc>{SITE}/{loc}</loc>", f"    <priority>{pr}</priority>",
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/{en}" />',
                    f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}/{ru}" />',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{en}" />', "  </url>"]
    out.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")
    print("wrote sitemap.xml")


sitemap()
