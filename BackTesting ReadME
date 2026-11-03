full = tables["Full period"]
def row(m):
    f = (lambda v: f"{v:.2f}") if m == "Sharpe" else (lambda v: f"{v:.2%}")
    return f"| {m} | {f(full.loc[m, 'Portfolio'])} | {f(full.loc[m, 'FTSE 100 (ISF.L)'])} |"

readme = f"""# Model portfolio: quality-momentum equity screen

A £5m portfolio of {len(w)} UK and European large caps for a balanced UK client with a 10-year horizon, built with a
systematic screen and backtested against the FTSE 100.

## What it does
1. **Night 1** (`night1_screen.ipynb`): screens the FTSE 100 + Euro Stoxx 50 (~150 stocks) in GBP on 12-1 momentum,
   quality (ROE, debt/equity) and low volatility, z-scores and averages them, and ranks the top 30.
2. **Selection**: picks the final holdings under the mandate (max 25% per sector, UK/Europe mix, no tobacco or weapons).
3. **Night 2** (`night2_backtest.ipynb`): equal weights, monthly rebalancing, 0.10% costs on turnover, and charts.

## How to run
Open the notebooks in Google Colab and run the cells top to bottom. Outputs are saved to a Google Drive folder.

## Data
Yahoo Finance via `yfinance`: adjusted daily prices (dividends included), fundamentals, and EURGBP=X for FX.
Benchmark: `ISF.L` adjusted close as a FTSE 100 total-return proxy.

## Results ({port.index[0].date()} to {port.index[-1].date()}, net of costs, risk-free {RISK_FREE:.2%})
| Metric | Portfolio | FTSE 100 |
|---|---|---|
{row("Total return")}
{row("CAGR")}
{row("Volatility")}
{row("Sharpe")}

## Limitations
- **Survivorship bias:** the universe is today's index members, so stocks that fell out of the indices are missing and the backtest flatters results.
- **Look-ahead bias:** fundamentals are today's values applied to the whole history, so the stock selection uses information that was not available at the time. The half-period split is a consistency check, not out-of-sample validation.
- **Data quality:** Yahoo Finance data can contain errors, and short-history stocks shorten the backtest window.
- **Costs:** 0.10% on turnover only; no taxes, bid-ask spreads or market impact.
"""
with open(path("README.md"), "w") as f:
    f.write(readme)
print(readme)
