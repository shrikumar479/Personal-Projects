top = ranked.head(TOP_N).reset_index()
out = pd.DataFrame({
    "rank": np.arange(1, len(top) + 1),
    "ticker": top["ticker"],
    "name": top["name"],
    "sector": top["sector"],
    "industry": top["industry"],
    "country": top["country"],
    "score": top["score"].round(3),
    "momentum_12_1": top["momentum"].round(3),
    "roe": top["returnOnEquity"].round(3),
    "debt_to_equity": top["debtToEquity"].round(1),
    "vol_1y": top["vol_1y"].round(3),
    "trailing_pe": top["trailingPE"].round(1),
    "market_cap_gbp_bn": (top["mcap_gbp"] / 1e9).round(1),
    "years_history": top["years_history"].round(1),
    "dcf_candidate": top["dcf_candidate"],
})
out.to_csv(path("shortlist.csv"), index=False)
print(f"Saved {path('shortlist.csv')}")
out
