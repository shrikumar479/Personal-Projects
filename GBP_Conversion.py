px = prices.ffill(limit=5)                        # bridge differing exchange holidays
fx = eurgbp.reindex(px.index).ffill().bfill()

gbp, unsupported = {}, []
for t in px.columns:
    cur = fund.loc[t, "currency"] if t in fund.index else np.nan
    if cur in ("GBp", "GBX"):
        gbp[t] = px[t] / 100
    elif cur == "GBP":
        gbp[t] = px[t]
    elif cur == "EUR":
        gbp[t] = px[t] * fx
    else:
        unsupported.append((t, cur))

px_gbp = pd.DataFrame(gbp)
px_gbp.to_csv(path("prices_gbp.csv"))
print("Dropped for currency:", unsupported)

jumps = (px_gbp.pct_change(fill_method=None).abs() > 0.4).sum()
print("Tickers with a daily move over 40% (inspect these):")
print(jumps[jumps > 0])
