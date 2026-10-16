"""
How much of a UK graduate's take-home pay goes on rent, city by city.

Pulled the median graduate salary, worked out take-home pay after tax + NI,
then compared it to average room rents in 14 cities to see who's actually
getting squeezed.

Yogesh Dahiwal
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# Median UK graduate salary, HESA Graduate Outcomes (2022/23 cohort, full-time
# first-degree grads, 15 months out).
GROSS_SALARY = 28_500

# Average monthly room rent incl. bills, SpareRoom Rental Index Q3 2026.
RENT = {
    "London (Inner)": 1002, "Edinburgh": 894, "Bath": 853, "Oxford": 834,
    "Cambridge": 792, "York": 750, "Bristol": 746, "Manchester": 685,
    "Gloucester": 642, "Birmingham": 614, "Leeds": 578, "Liverpool": 554,
    "Sheffield": 540, "Hull": 507,
}

# 2025/26 England bands
PERSONAL_ALLOWANCE = 12_570   # tax-free
NI_THRESHOLD = 12_570         # primary threshold

income_tax = max(0, GROSS_SALARY - PERSONAL_ALLOWANCE) * 0.20   # basic rate 20%
national_ins = max(0, GROSS_SALARY - NI_THRESHOLD) * 0.08       # 8% main rate

net_year = GROSS_SALARY - income_tax - national_ins
net_month = net_year / 12

print(f"Gross salary:        £{GROSS_SALARY:,.0f}")
print(f"Income tax:          £{income_tax:,.0f}")
print(f"National Insurance:  £{national_ins:,.0f}")
print(f"Take-home / year:    £{net_year:,.0f}")
print(f"Take-home / month:   £{net_month:,.2f}\n")

# rent as a % of take-home, cheapest city first
rows = sorted(RENT.items(), key=lambda kv: kv[1])
cities = [c for c, _ in rows]
share = [rent / net_month * 100 for _, rent in rows]

for c, r in rows:
    print(f"{c:<16} £{r:>5}  ->  {r / net_month * 100:>4.0f}% of take-home")

# --- chart ---

def _font(path):
    return fm.FontProperties(fname=path) if path and os.path.isfile(path) else None

_FONT_DIRS = [
    "/usr/share/fonts/truetype/google-fonts/",          # Linux (if present)
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts") + os.sep,  # Windows, per-user
    os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts") + os.sep,                      # Windows, system
]

def _find_font(filename):
    for d in _FONT_DIRS:
        candidate = os.path.join(d, filename)
        if os.path.isfile(candidate):
            return _font(candidate)
    return None

f_bold = _find_font("Poppins-Bold.ttf")
f_med  = _find_font("Poppins-Medium.ttf")
f_reg  = _find_font("Poppins-Regular.ttf")

BG, TEAL, TEAL_D, WHITE, GREY, HI = "#0E1222", "#2AB6D0", "#1F7E95", "#EDF1F8", "#96A2B9", "#F4A62A"

fig, ax = plt.subplots(figsize=(10.2, 8.4), dpi=130)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

colors = [HI if c == "Gloucester" else (TEAL_D if p < 30 else TEAL)
          for c, p in zip(cities, share)]
bars = ax.barh(cities, share, color=colors, height=0.68, zorder=3)

ax.axvline(30, color="#5A6480", lw=1.4, ls=(0, (5, 4)), zorder=2)
ax.text(30, len(cities) - 0.3, "  30% — common affordability line",
        color="#8A96AD", fontproperties=f_reg, fontsize=11, va="bottom", ha="left")

for b, p in zip(bars, share):
    ax.text(b.get_width() - 1.3, b.get_y() + b.get_height() / 2, f"{p:.0f}%",
            va="center", ha="right",
            color="#06202A" if p >= 30 else WHITE,
            fontproperties=f_med, fontsize=12.5, zorder=4)

ax.set_xlim(0, 55)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0, labelcolor=WHITE)
ax.tick_params(axis="x", length=0, labelbottom=False)
for lbl in ax.get_yticklabels():
    if f_med: lbl.set_fontproperties(f_med)
    lbl.set_fontsize(12.5)
    if lbl.get_text() == "Gloucester":
        lbl.set_color(HI)
ax.set_axisbelow(True)

fig.text(0.045, 0.965, "Where can a UK graduate actually afford to live?",
         fontproperties=f_bold, fontsize=19, color=WHITE)
fig.text(0.045, 0.925, "Share of a graduate's take-home pay spent on an average room, by city",
         fontproperties=f_reg, fontsize=12.5, color=GREY)
fig.text(0.045, 0.038,
         "Rent: SpareRoom avg room (incl. bills), Q3 2026  ·  Salary: £28,500 median graduate (HESA)  ·  Take-home after tax + NI, 2025/26",
         fontproperties=f_reg, fontsize=9.3, color="#6D7890")
fig.text(0.955, 0.918, "Yogesh Dahiwal", fontproperties=f_med, fontsize=11, color=TEAL, ha="right")

plt.subplots_adjust(left=0.19, right=0.965, top=0.885, bottom=0.075)
plt.savefig("chart.png", facecolor=BG)
print("\nSaved chart.png")
