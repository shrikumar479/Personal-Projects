d = universe.reindex(prices.columns).join(fund.rename(columns={"country": "yahoo_country"}))
d.index.name = "ticker"
g = px_gbp.reindex(columns=d.index)
rets = g.pct_change(fill_method=None).iloc[-252:]

d["momentum"] = g.iloc[-1 - MOM_SKIP] / g.iloc[-1 - MOM_LOOKBACK] - 1
d["vol_1y"] = (rets.std() * np.sqrt(252)).where(rets.count() >= 200)
first = pd.to_datetime(g.apply(lambda s: s.first_valid_index()))
d["years_history"] = (g.index[-1] - first).dt.days / 365.25

d["mcap_gbp"] = np.where(d["currency"] == "EUR", d["marketCap"] * fx.iloc[-1], d["marketCap"])
d["is_bank_or_insurer"] = d["industry"].fillna("").str.contains("Bank|Insurance", case=False)
d["dcf_candidate"] = ~d["is_bank_or_insurer"]

print("Smallest / largest market caps (GBP bn):")
caps = (d["mcap_gbp"] / 1e9).round(1).dropna().sort_values()
print(pd.concat([caps.head(5), caps.tail(5)]).to_string())

# Filters: each stock gets the first reason it fails
d["drop_reason"] = ""
def flag(mask, why):
    d.loc[mask & (d["drop_reason"] == ""), "drop_reason"] = why

flag(g.iloc[-1].isna(), "no recent GBP price")
flag(d["momentum"].isna(), "not enough history for 12-1 momentum")
flag(d["returnOnEquity"].isna(), "missing ROE")
flag(d["marketCap"].isna(), "missing market cap")
flag(d["sector"].isna(), "missing sector")
if USE_LOW_VOL:
    flag(d["vol_1y"].isna(), "missing volatility")
flag(d["dcf_candidate"] & d["debtToEquity"].isna(), "missing debt/equity")
flag(d["dcf_candidate"] & (d["debtToEquity"] < 0), "negative equity (debt/equity < 0)")
flag(d["mcap_gbp"] < MIN_MCAP_GBP, "market cap below minimum")

kept = d[d["drop_reason"] == ""].copy()
d[d["drop_reason"] != ""][["name", "drop_reason"]].to_csv(path("dropped.csv"))
print(f"\n{len(d)} stocks -> {len(kept)} pass the filters")
print(d["drop_reason"].replace("", "KEPT").value_counts())
