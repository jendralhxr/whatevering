import matplotlib.pyplot as plt
import yfinance as yf

TICKERS = {
    "IHSG": "^JKSE",
    "BBRI": "BBRI.JK", "BBCA": "BBCA.JK", "DCII": "DCII.JK",
    "BMRI": "BMRI.JK", "CASA": "CASA.JK",
    "BBNI": "BBNI.JK", "ENRG": "ENRG.JK",
}

# Pull ~1 month so we always have at least 7 trading days, then keep the last 7
raw = yf.download(list(TICKERS.values()), period="1mo", interval="1d",
                  auto_adjust=False, progress=False)["Close"]
close = raw.rename(columns={v: k for k, v in TICKERS.items()})[list(TICKERS)]
close = close.dropna(how="all").tail(7)
close.index = close.index.strftime("%d %b")

print(close.round(2).to_string())

# Figure 1: each instrument in absolute price (own y-axis, since IHSG ~5,800 vs stocks ~100s-6,000)
fig, axes = plt.subplots(3, 3, figsize=(14, 9), sharex=True)
for ax, col in zip(axes.ravel(), close.columns):
    s = close[col]
    ax.plot(s.index, s.values, marker="o", linewidth=1.8)
    chg = (s.dropna().iloc[-1] / s.dropna().iloc[0] - 1) * 100
    ax.set_title(f"{col}  ({chg:+.2f}%)", fontsize=11)
    ax.grid(alpha=0.3)
    ax.tick_params(axis="x", rotation=45)
fig.suptitle("IHSG & selected IDX stocks - last 7 trading days (close, IDR)", fontsize=14)
fig.tight_layout()

# Figure 2: rebased to 100 so performance is comparable on one chart
rebased = close / close.bfill().iloc[0] * 100
fig2, ax2 = plt.subplots(figsize=(12, 6))
for col in rebased.columns:
    ax2.plot(rebased.index, rebased[col], marker="o", linewidth=2.5 if col == "IHSG" else 1.4,
             color="black" if col == "IHSG" else None, label=col)
ax2.axhline(100, color="gray", linestyle="--", linewidth=0.8)
ax2.set_title("Last 7 trading days, rebased to 100")
ax2.set_ylabel("Index (first day = 100)")
ax2.grid(alpha=0.3)
ax2.legend(ncol=3)
fig2.tight_layout()
