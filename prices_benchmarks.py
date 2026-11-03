px_all = pd.read_csv(path("prices_gbp.csv"), index_col=0, parse_dates=True)
px = px_all[tickers]

first_valid = pd.to_datetime(px.apply(lambda s: s.first_valid_index()))
assert first_valid.notna().all(), "a holding has no price data at all"
start = first_valid.max()
if BACKTEST_START is not None:
    start = max(start, pd.Timestamp(BACKTEST_START))
print(f"Backtest starts {start.date()} (latest first price: {first_valid.idxmax()})")
px = px.loc[start:].ffill()
assert px.isna().sum().sum() == 0, "gaps left in prices"

# Benchmark
if os.path.exists(path("benchmark_prices.csv")):
    bpx = pd.read_csv(path("benchmark_prices.csv"), index_col=0, parse_dates=True).iloc[:, 0]
else:
    raw = yf.download(BENCH_TICKER, period="10y", auto_adjust=True, progress=False)["Close"]
    bpx = raw.iloc[:, 0] if isinstance(raw, pd.DataFrame) else raw
    bpx.index = pd.to_datetime(bpx.index).tz_localize(None)
    bpx.rename(BENCH_TICKER).to_csv(path("benchmark_prices.csv"))

# Put the benchmark on the portfolio's calendar (UK holidays become 0% days, so nothing is dropped)
bpx = bpx.reindex(px.index, method="ffill")
assert bpx.notna().all(), "benchmark starts after the portfolio"
print(f"{px.shape[1]} holdings, {len(px)} days, {px.index[0].date()} to {px.index[-1].date()}")
