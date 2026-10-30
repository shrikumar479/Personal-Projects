FIELDS = ["longName", "marketCap", "returnOnEquity", "debtToEquity", "trailingPE",
          "sector", "industry", "country", "currency", "financialCurrency"]
NUMERIC = ["marketCap", "returnOnEquity", "debtToEquity", "trailingPE"]

def get_info(t, retries=3):
    for i in range(retries):
        try:
            info = yf.Ticker(t).info
            if info and len(info) > 5:
                return {k: info.get(k) for k in FIELDS}
        except Exception:
            pass
        time.sleep(2 * (i + 1))
    return None

cache = (pd.read_csv(path("fundamentals.csv"), index_col=0).to_dict("index")
         if os.path.exists(path("fundamentals.csv")) else {})
todo = [t for t in prices.columns if t not in cache or pd.isna(cache[t].get("currency"))]
print(f"Fetching {len(todo)} tickers ({len(cache)} already cached)")

for t in tqdm(todo):
    cache[t] = get_info(t) or {k: np.nan for k in FIELDS}
    time.sleep(0.5)

fund = pd.DataFrame.from_dict(cache, orient="index")[FIELDS]
fund.index.name = "ticker"
fund.to_csv(path("fundamentals.csv"))
for c in NUMERIC:
    fund[c] = pd.to_numeric(fund[c], errors="coerce").replace([np.inf, -np.inf], np.nan)

print(fund.isna().sum())
fund.head()
