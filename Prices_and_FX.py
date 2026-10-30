HEADERS = {"User-Agent": "Mozilla/5.0 (student model-portfolio project)"}

def wiki_tables(url):
    html = requests.get(url, headers=HEADERS, timeout=30).text
    return pd.read_html(io.StringIO(html))

def find_table(tables, wanted, min_rows):
    """First table with at least min_rows rows whose columns match every group in `wanted`."""
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if len(t) >= min_rows and all(any(k in c for c in cols for k in alts) for alts in wanted):
            return t
    raise ValueError(f"No table found with columns matching {wanted}")

def col(df, *keys):
    return next(c for c in df.columns if any(k in str(c).lower() for k in keys))

def epic_to_yahoo(epic):
    t = re.sub(r"\[.*?\]", "", str(epic)).strip().upper()   # drop footnote markers
    if t.endswith(".L"):
        return t
    return t.rstrip(".").replace(".", "-") + ".L"          # "BP." -> BP.L, "BT.A" -> BT-A.L

# FTSE 100
ftse_raw = find_table(wiki_tables("https://en.wikipedia.org/wiki/FTSE_100_Index"),
                      [("company",), ("ticker", "epic")], min_rows=90)
ftse = pd.DataFrame({
    "ticker": ftse_raw[col(ftse_raw, "ticker", "epic")].map(epic_to_yahoo),
    "name": ftse_raw[col(ftse_raw, "company")],
    "country": "United Kingdom",
    "index": "FTSE 100",
})

# Euro Stoxx 50
eu_raw = find_table(wiki_tables("https://en.wikipedia.org/wiki/EURO_STOXX_50"),
                    [("ticker",), ("name",), ("registered",)], min_rows=40)
eu = pd.DataFrame({
    "ticker": eu_raw[col(eu_raw, "ticker")].astype(str).str.strip(),
    "name": eu_raw[col(eu_raw, "name")],
    "country": eu_raw[col(eu_raw, "registered")],
    "index": "Euro Stoxx 50",
})

universe = pd.concat([ftse, eu], ignore_index=True).drop_duplicates("ticker").set_index("ticker")
universe.to_csv(path("universe.csv"))
print(universe["index"].value_counts())
universe.head()
