!pip install -q --upgrade yfinance lxml

import io, os, re, time, warnings
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from tqdm.auto import tqdm
warnings.filterwarnings("ignore")

# Persist everything to Drive; fall back to the current folder outside Colab
try:
    from google.colab import drive
    drive.mount("/content/drive")
    OUT_DIR = "/content/drive/MyDrive/model-portfolio-2026"
except ImportError:
    OUT_DIR = "."
os.makedirs(OUT_DIR, exist_ok=True)
def path(name): return os.path.join(OUT_DIR, name)

# ---------------- Settings ----------------
YEARS = 10                    # price history to download
MIN_MCAP_GBP = 5e9            # drop anything smaller than 5bn GBP
USE_LOW_VOL = True            # optional third factor: lower 1-year volatility is better
TOP_N = 30                    # shortlist size
MOM_LOOKBACK = 252            # about 12 months of trading days
MOM_SKIP = 21                 # skip the latest month (the "-1" in 12-1)
