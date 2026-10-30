# ==== NEW CELL: paste after cell 9. Needs `out`, `check_selection`, `path` from earlier cells. ====
# Flags banks/insurers for the DCF person, then proposes the final 15 from the top 30.

# ---------------- Settings ----------------
N_FINAL = 15
MAX_SECTOR_PCT = 0.25
MAX_PER_SECTOR = int(N_FINAL * MAX_SECTOR_PCT)   # 3 of 15 (a 4th would be 26.7%, over the cap)
MAX_UK, MAX_EUROPE = 10, 10                      # at 15 names this guarantees at least 5 of each
MIN_HISTORY_YEARS = 9.5                          # needed for the 10-year backtest on Night 2

# Client ethics: no tobacco or weapons. Confirm the weapons list with the Lead.
EXCLUDE_INDUSTRIES = ["Tobacco"]
EXCLUDE_TICKERS = ["BA.L", "RHM.DE"]             # BAE Systems, Rheinmetall

# ---------------- Flags ----------------
sl = out.copy()                                  # already ranked best-first by score
sl["dcf_note"] = np.where(sl["dcf_candidate"], "OK for DCF", "Unsuitable: bank/insurer")
sl["ethical_exclude"] = sl["industry"].isin(EXCLUDE_INDUSTRIES) | sl["ticker"].isin(EXCLUDE_TICKERS)

print("Banks/insurers (unsuitable for DCF):", sl.loc[~sl["dcf_candidate"], "ticker"].tolist())
print("Excluded on ethics:", sl.loc[sl["ethical_exclude"], ["rank", "ticker", "name"]].values.tolist() or "none")

# ---------------- Greedy pick: walk down the ranking, skip anything that breaks a rule ----------------
def pick(df, n, need_history=True, use_country_caps=True):
    chosen, sectors, uk, eu = [], {}, 0, 0
    for _, r in df.iterrows():
        if len(chosen) == n:
            break
        if r["ethical_exclude"]:
            continue
        if need_history and r["years_history"] < MIN_HISTORY_YEARS:
            continue
        if sectors.get(r["sector"], 0) >= MAX_PER_SECTOR:
            continue
        is_uk = r["country"] == "United Kingdom"
        if use_country_caps and ((is_uk and uk >= MAX_UK) or (not is_uk and eu >= MAX_EUROPE)):
            continue
        chosen.append(r["ticker"])
        sectors[r["sector"]] = sectors.get(r["sector"], 0) + 1
        uk += is_uk
        eu += (not is_uk)
    return chosen

final = pick(sl, N_FINAL)
if len(final) < N_FINAL:
    print("Not enough names: relaxing the 10-year history rule")
    final = pick(sl, N_FINAL, need_history=False)
if len(final) < N_FINAL:
    print("Still not enough: relaxing the UK/Europe caps")
    final = pick(sl, N_FINAL, need_history=False, use_country_caps=False)
if len(final) < N_FINAL:
    print(f"WARNING: only {len(final)} names pass. Set TOP_N = 40 in cell 1 and re-run from cell 6.")

# ---------------- Result ----------------
final_df = sl.set_index("ticker").loc[final].reset_index()
final_df.to_csv(path("final_selection.csv"), index=False)
short = final_df.loc[final_df["years_history"] < MIN_HISTORY_YEARS, "ticker"].tolist()
if short:
    print("Under 10 years of data (Night 2 will need a note or a swap):", short)

check_selection(final)
final_df[["rank", "ticker", "name", "sector", "country", "score", "years_history", "dcf_note"]]
