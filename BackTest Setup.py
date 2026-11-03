!pip install -q --upgrade yfinance

import os, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
import yfinance as yf
warnings.filterwarnings("ignore")

try:
    from google.colab import drive
    drive.mount("/content/drive")
    OUT_DIR = "/content/drive/MyDrive/model-portfolio-2026"
except ImportError:
    OUT_DIR = "."
os.makedirs(OUT_DIR, exist_ok=True)
def path(name): return os.path.join(OUT_DIR, name)

# ---------------- Settings ----------------
FINAL_TICKERS = None          # e.g. ["AZN.L", "SAP.DE", ...]; None = use final_selection.csv from Night 1
COST = 0.001                  # 0.10% per unit of turnover
RISK_FREE = 0.04              # REPLACE with the group's agreed UK 10-year gilt yield, as a decimal
START_VALUE = 5_000_000
BENCH_TICKER = "ISF.L"        # iShares FTSE 100 ETF, adjusted close = total-return proxy (benchmark only)
BACKTEST_START = None         # None = first date every holding has a price, or e.g. "2017-01-01"
EXCLUDE_TICKERS = ["BA.L", "RHM.DE"]   # weapons names from the Night 1 selection cell

# Chart colours: REPLACE with Ops's hex codes
COLOR_PORT, COLOR_BENCH, COLOR_NEG = "#1F3A5F", "#9AA5B1", "#B23A48"
