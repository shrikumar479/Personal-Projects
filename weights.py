scores = pd.read_csv(path("scores_all.csv"), index_col=0)
if FINAL_TICKERS is None:
    FINAL_TICKERS = pd.read_csv(path("final_selection.csv"))["ticker"].tolist()
tickers = list(FINAL_TICKERS)

missing = [t for t in tickers if t not in scores.index]
assert not missing, f"Not in scores_all.csv (typo, or filtered out on Night 1): {missing}"

w = scores.loc[tickers, ["name", "sector", "country", "score"]].copy()
w.index.name = "ticker"
w["weight"] = 1 / len(w)
w = w[["name", "sector", "country", "weight", "score"]]

# Mandate checks
sector_w = w.groupby("sector")["weight"].sum()
assert 15 <= len(w) <= 20, f"{len(w)} holdings, need 15-20"
assert w.index.is_unique, "duplicate tickers"
assert abs(w["weight"].sum() - 1) < 1e-9, "weights don't sum to 1"
assert w["weight"].max() <= 0.10, "a stock is over 10%"
assert sector_w.max() <= 0.25 + 1e-9, f"sector over 25%: {sector_w[sector_w > 0.25].to_dict()}"
assert not (set(tickers) & set(EXCLUDE_TICKERS)), "weapons name in the portfolio"
assert not (scores.loc[tickers, "industry"] == "Tobacco").any(), "tobacco name in the portfolio"

w.to_csv(path("weights.csv"))
print(f"{len(w)} holdings, {w['weight'].iloc[0]:.2%} each. Saved weights.csv: post it now.")
print("\nSector weights:\n", (sector_w * 100).round(1).astype(str) + "%")
print("\nCountry mix:", w["country"].value_counts().to_dict())
w
