import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.stats import linregress
except ModuleNotFoundError:
    def linregress(x, y):
        x = pd.Series(x, dtype="float64")
        y = pd.Series(y, dtype="float64")
        x_diff = x - x.mean()
        y_diff = y - y.mean()
        slope = (x_diff * y_diff).sum() / (x_diff ** 2).sum()
        intercept = y.mean() - slope * x.mean()
        return slope, intercept, None, None, None


def draw_plot():
    df = pd.read_csv("epa-sea-level.csv")

    fig, ax = plt.subplots()
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    first_year = df["Year"].min()
    all_years = pd.Series(range(first_year, 2051))
    slope, intercept, _, _, _ = linregress(
        df["Year"], df["CSIRO Adjusted Sea Level"]
    )
    ax.plot(all_years, slope * all_years + intercept)

    recent_df = df[df["Year"] >= 2000]
    recent_years = pd.Series(range(2000, 2051))
    recent_slope, recent_intercept, _, _, _ = linregress(
        recent_df["Year"], recent_df["CSIRO Adjusted Sea Level"]
    )
    ax.plot(recent_years, recent_slope * recent_years + recent_intercept)

    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    fig.savefig("sea_level_plot.png")
    return ax
