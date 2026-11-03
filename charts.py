CHART_DIR = path("charts")
os.makedirs(CHART_DIR, exist_ok=True)

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "figure.facecolor": "white"})

def save_chart(fig, name):
    fig.savefig(os.path.join(CHART_DIR, name), dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    plt.close(fig)

# 1. Growth of 5m
gp = START_VALUE * (1 + port).cumprod()
gb = START_VALUE * (1 + bench).cumprod()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(gp.index, gp, color=COLOR_PORT, lw=1.8, label="Portfolio (net of costs)")
ax.plot(gb.index, gb, color=COLOR_BENCH, lw=1.8, label="FTSE 100 total return (ISF.L)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"£{x / 1e6:.1f}m"))
ax.set_title("Growth of £5m: portfolio vs FTSE 100", loc="left", fontweight="bold")
ax.legend(frameon=False)
save_chart(fig, "01_growth_of_5m.png")

# 2. Sector weights
sec = (w.groupby("sector")["weight"].sum().sort_values())
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(sec.index, sec.values, color=COLOR_PORT)
ax.axvline(0.25, color=COLOR_NEG, ls="--", lw=1)
ax.text(0.25, 1.0, " 25% cap", transform=ax.get_xaxis_transform(), color=COLOR_NEG, va="bottom", fontsize=9)
for y, v in enumerate(sec.values):
    ax.text(v + 0.003, y, f"{v:.1%}", va="center", fontsize=9)
ax.xaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_xlim(0, max(0.30, sec.max() + 0.05))
ax.grid(axis="y", visible=False)
ax.set_title("Sector weights", loc="left", fontweight="bold")
save_chart(fig, "02_sector_weights.png")

# 3. Country split
cty = (w.groupby("country")["weight"].sum().sort_values())
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(cty.index, cty.values, color=COLOR_PORT)
for y, v in enumerate(cty.values):
    ax.text(v + 0.003, y, f"{v:.1%}", va="center", fontsize=9)
ax.xaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_xlim(0, cty.max() + 0.08)
ax.grid(axis="y", visible=False)
ax.set_title("Country split (by listing / registered office)", loc="left", fontweight="bold")
save_chart(fig, "03_country_split.png")

# 4. Rolling 12-month excess return
m = pd.DataFrame({"p": (1 + port).cumprod(), "b": (1 + bench).cumprod()}).resample("ME").last()
roll = (m["p"].pct_change(12) - m["b"].pct_change(12)).dropna()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(roll.index, roll.values, width=20, color=[COLOR_PORT if v >= 0 else COLOR_NEG for v in roll.values])
ax.axhline(0, color="black", lw=0.8)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_title("Rolling 12-month excess return vs FTSE 100", loc="left", fontweight="bold")
save_chart(fig, "04_rolling_12m_excess.png")

print("Saved:", sorted(os.listdir(CHART_DIR)))
