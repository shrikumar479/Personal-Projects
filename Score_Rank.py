def zscore(s):
    return ((s - s.mean()) / s.std(ddof=0)).clip(-3, 3)

kept["z_momentum"] = zscore(kept["momentum"])
kept["z_roe"] = zscore(kept["returnOnEquity"])
kept["z_leverage"] = zscore(-kept["debtToEquity"].where(kept["dcf_candidate"]))   # lower debt is better
if USE_LOW_VOL:
    kept["z_lowvol"] = zscore(-kept["vol_1y"])                                     # lower vol is better

zcols = [c for c in kept.columns if c.startswith("z_")]
kept["score"] = kept[zcols].mean(axis=1, skipna=True)

ranked = kept.sort_values("score", ascending=False)
ranked.to_csv(path("scores_all.csv"))          # full scored universe, reused for the holdings table on Night 3
print("Factors in composite:", zcols)
