def stats(r, rf=RISK_FREE):
    years = (r.index[-1] - r.index[0]).days / 365.25
    total = (1 + r).prod() - 1
    cagr = (1 + total) ** (1 / years) - 1
    vol = r.std() * np.sqrt(len(r) / years)
    return {"Total return": total, "CAGR": cagr, "Volatility": vol, "Sharpe": (cagr - rf) / vol}

def compare(p, b):
    t = pd.DataFrame({"Portfolio": stats(p), "FTSE 100 (ISF.L)": stats(b)})
    t["Difference"] = t["Portfolio"] - t["FTSE 100 (ISF.L)"]
    return t

mid = port.index[len(port) // 2]
tables = {
    "Full period": compare(port, bench),
    f"First half (to {mid.date()})": compare(port[:mid], bench[:mid]),
    "Second half": compare(port[mid:].iloc[1:], bench[mid:].iloc[1:]),
}
results = pd.concat(tables)
results.to_csv(path("backtest_results.csv"))

def fmt(t):
    f = t.astype(object)
    for c in t.columns:
        f[c] = [f"{v:.2f}" if m == "Sharpe" else f"{v:.2%}" for m, v in t[c].items()]
    return f

for name, t in tables.items():
    print(f"\n{name}")
    print(fmt(t).to_string())

excess = tables["Full period"].loc["CAGR", "Difference"]
print(f"\nNet excess CAGR vs benchmark: {excess:.2%} a year (client target: 1-2% net)")
