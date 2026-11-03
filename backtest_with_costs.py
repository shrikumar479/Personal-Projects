def backtest(px, w, cost):
    """Daily portfolio returns, rebalanced to w at the start of every month."""
    w = w.reindex(px.columns)
    rets = px.pct_change().iloc[1:]
    pieces, turnovers, w_drift = [], [], None
    for _, blk in rets.groupby(rets.index.to_period("M")):
        turnover = 1.0 if w_drift is None else float((w - w_drift).abs().sum())
        growth = (1 + blk).cumprod()
        val = growth.mul(w, axis=1).sum(axis=1)          # value of 1 split by w at the month start
        day = val.pct_change()
        day.iloc[0] = (1 - cost * turnover) * val.iloc[0] - 1
        w_drift = growth.iloc[-1] * w / val.iloc[-1]     # weights after drifting through the month
        pieces.append(day)
        turnovers.append(turnover)
    return pd.concat(pieces), turnovers

wt = w["weight"]
port, turnovers = backtest(px, wt, COST)
port_gross, _ = backtest(px, wt, 0.0)
bench = bpx.pct_change().iloc[1:]

assert port.index.equals(bench.index), "portfolio and benchmark dates don't match"
assert not port.isna().any() and not bench.isna().any(), "NaNs in returns"

port.rename("portfolio_return").rename_axis("date").to_csv(path("portfolio_daily_returns.csv"))
bench.rename("benchmark_return").rename_axis("date").to_csv(path("benchmark_daily_returns.csv"))

years = (port.index[-1] - port.index[0]).days / 365.25
cagr_net = (1 + port).prod() ** (1 / years) - 1
cagr_gross = (1 + port_gross).prod() ** (1 / years) - 1
print(f"Saved both return files: {len(port)} rows, {port.index[0].date()} to {port.index[-1].date()} ({years:.1f} years)")
print(f"Average monthly turnover after the first month: {np.mean(turnovers[1:]):.1%}")
print(f"CAGR gross {cagr_gross:.2%}, net {cagr_net:.2%}, cost drag {(cagr_gross - cagr_net) * 1e4:.0f} bp a year")
print("Tell Risk: portfolio_daily_returns.csv is NET of 10bp costs; benchmark is ISF.L total return.")
