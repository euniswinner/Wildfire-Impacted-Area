
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("county_fire_elevation.csv")
df = df.dropna(subset=["mean_elevation_m", "SUM_Area_Acres"])

x = df["mean_elevation_m"].to_numpy(dtype=float)
y = df["SUM_Area_Acres"].to_numpy(dtype=float)
n = len(x)


r = np.corrcoef(x, y)[0, 1]

# t-statistic for testing whether r is significantly different from 0
t_stat = r * math.sqrt((n - 2) / (1 - r**2))
df_freedom = n - 2



def _betacf(a, b, x, max_iter=200, eps=1e-10):
    """Continued fraction for the incomplete beta function (Numerical Recipes)."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d, c = 1.0 / d, c
        h *= d * c

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d, c = 1.0 / d, c
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    """Regularized incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_beta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(ln_beta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    else:
        return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_dist_two_tailed_pvalue(t_stat, deg_free):
    """Two-tailed p-value for a t-statistic (replacement for scipy.stats.ttest)."""
    x_beta = deg_free / (deg_free + t_stat**2)
    return _betai(deg_free / 2.0, 0.5, x_beta)


p_value = t_dist_two_tailed_pvalue(t_stat, df_freedom)


slope, intercept = np.polyfit(x, y, 1)
r_squared = r**2

print(f"Pearson correlation coefficient (r): {r:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"Regression equation: burned_acres = {slope:.2f} * elevation_m + {intercept:.2f}")
print(f"R-squared: {r_squared:.3f}")

if p_value < 0.05:
    print(">> Statistically significant correlation (p < 0.05)")
else:
    print(">> Not statistically significant (p >= 0.05) — check sample size or data quality")

sns.set_theme(style="whitegrid")
plt.figure(figsize=(9, 6))

sns.regplot(
    x=x, y=y,
    scatter_kws={"color": "#d95f02", "alpha": 0.7, "edgecolor": "black"},
    line_kws={"color": "#7570b3"}
)

top_counties = df.nlargest(5, "SUM_Area_Acres")
for _, row in top_counties.iterrows():
    plt.annotate(
        row["NAME"],
        (row["mean_elevation_m"], row["SUM_Area_Acres"]),
        textcoords="offset points", xytext=(5, 5), fontsize=8
    )

plt.title(
    f"Elevation vs. Cumulative Wildfire Damage by County\n(r = {r:.2f}, p = {p_value:.4f})",
    fontsize=14, fontweight="bold"
)
plt.xlabel("Mean Elevation (m)", fontsize=11, fontweight="bold")
plt.ylabel("Cumulative Burned Area (Acres)", fontsize=11, fontweight="bold")
plt.figtext(0.99, 0.01, "Source: CAL FIRE, USGS 3DEP DEM (via ArcGIS Pro Zonal Statistics)",
            ha="right", fontsize=8, style="italic", color="gray")

plt.tight_layout()
plt.savefig("elevation_wildfire_correlation.png", dpi=300, bbox_inches="tight")
plt.show()


summary = df[["NAME", "mean_elevation_m", "SUM_Area_Acres"]].sort_values(
    "SUM_Area_Acres", ascending=False
)
summary.to_csv("elevation_fire_summary.csv", index=False)
print("\nSummary table saved: elevation_fire_summary.csv")
