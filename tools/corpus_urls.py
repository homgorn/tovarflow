"""Canonical URL inventory for the Q-Parser documentation corpus.

The public sitemap contains thousands of /catalog/<city>/<category> permutations.
Those are catalogue views, not documentation, so they are intentionally excluded.
This inventory covers every knowledge-base page plus the commercial and
policy pages needed to design the storefront / marketplace pipeline.
"""

BASE = "https://q-parser.ru"

FORMAT_SLUGS = [
    "advantshopv1format", "advantshopv2format", "alltradesformat", "amadyformat",
    "bitrixcsvformat", "botobotformat", "cmss3format", "commercemlformat",
    "cscartformat", "csvformat", "diskauntscsvformat", "epicentrkymlformat",
    "eshoperformat", "facebookcsvformat", "facebookxmlfeedformat",
    "googlemerchantformat", "hostcmsformat", "insalescsvformat", "insalesxlsformat",
    "joomlaformat", "joomshoppingformat", "jsonformat", "kaspixmlformat",
    "kupivspformat", "lpmotorformat", "materinstvoshopformat", "megamarketymlformat",
    "mikaiformat", "mogutaformat", "moyskladformat", "ok24format", "okalbumsformat",
    "okaycmsformat", "okformat", "opencartcsvliteformat", "opencartcsvpriceproformat",
    "opencartexportimportformat", "openmallformat", "osclassadimporterformat",
    "phpshopformat", "pokupki63format", "pokupkiprostoformat", "prestashopformat",
    "prestashopmagiconestoremanagerformat", "promuaymlformat", "readyscriptformat",
    "rozetkaymlformat", "samarskieroditeliformat", "serpokformat", "shopifyformat",
    "showcaseformat", "simplacmsformat", "spkostromaformat", "spprotonformat",
    "storelandformat", "stospformat", "supermamkiformat", "superpuperformat",
    "tildacsvformat", "tildaymlformat", "tom70format", "uralcmscsvformat",
    "ushopymlformat", "vkalbumsformat", "vkformat", "webasystshopscriptformat",
    "wixformat", "woocommerceformat", "xlsformat", "xmlformat", "ymlformat",
    "zaprosto24format",
]

MODS_SLUGS = [
    "price", "cols", "cols-replace", "cols-sort", "cols-rename", "cols-split",
    "cols-remove", "cols-cut", "cols-strip-html", "filter", "deduplication",
    "sort", "images", "images/resize", "images/embed", "images/text",
    "images/overlay", "images/cut", "images/count", "images/transparent",
    "images/background", "copying", "publish", "html-remove-children",
]

AI_SLUGS = [
    "agent", "images", "unwatermark", "web-search", "prompt-writing", "models", "points",
]

MISC_SLUGS = [
    "social", "referral", "button", "erange", "parser-categories", "filestorage",
    "file-headers", "parser-compare", "additional-css-selectors", "api", "format",
]

TOP_LEVEL = [
    ("/", "root", "landing"),
    ("/what-can", "root", "capabilities"),
    ("/tariffs", "root", "pricing"),
    ("/faq", "root", "faq"),
    ("/reviews", "root", "reviews"),
    ("/supplier", "root", "supplier"),
    ("/supplier/widget", "root", "supplier"),
    ("/agreement", "root", "legal"),
    ("/catalog", "root", "catalog"),
    ("/blog", "root", "blog"),
]


def _path(section: str, slug: str) -> str:
    return f"/howto/{section}/{slug}" if section else f"/howto/{slug}"


def inventory() -> list[dict]:
    items: list[dict] = []

    def add(path: str, section: str, kind: str) -> None:
        items.append({"url": BASE + path, "path": path, "section": section, "kind": kind})

    add("/howto", "howto", "index")
    for slug in FORMAT_SLUGS:
        add(_path("format", slug), "format", "format")
    add("/howto/automata", "automata", "guide")
    add("/howto/automata/edit", "automata", "guide")
    add("/howto/automata/webhooks", "automata", "guide")
    for slug in MODS_SLUGS:
        add(_path("mods", slug), "mods", "modifier")
    for slug in AI_SLUGS:
        add(_path("ai", slug), "ai", "ai")
    for slug in MISC_SLUGS:
        add(_path("", slug), "misc", "guide")
    for path, section, kind in TOP_LEVEL:
        add(path, section, kind)
    # de-duplicate while preserving order
    seen, out = set(), []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            out.append(item)
    return out


if __name__ == "__main__":
    inv = inventory()
    print(f"{len(inv)} canonical URLs")
    for i in inv:
        print(i["url"])
