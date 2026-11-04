import os
import re
import json
import sys
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter, LogLocator

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

BOUNDARY_FOLDER = "boundaries"

with open("data.json", "r") as file:
    data = json.load(file)

def progress_bar(iteration, total, prefix='', suffix='', length=90, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def clean_county_name(name: str):
    name = re.sub(r",\s*[A-Z]{2}$", "", name.strip())
    name = re.sub(r"\s+(County|Parish|Borough|Census Area)$", "", name, flags=re.IGNORECASE)
    return name.strip().casefold()

def save_map(fig, filename: str):
    path = os.path.join("export", filename)

    fig.savefig(path, dpi=1200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved: {path}")

states_geo = gpd.read_file("boundaries/tl_2024_us_state.zip")
counties_geo = gpd.read_file("boundaries/tl_2024_us_county.zip")

def graph_county_death_per_100_map():
    counties = []
    state_fips = []
    values = []

    for item in data:
        state = states_geo[
            states_geo["NAME"] == item["name"]
        ]

        if state.empty:
            continue

        fips = state.iloc[0]["STATEFP"]

        for county in item["counties"]:

            counties.append(clean_county_name(county["name"]))
            state_fips.append(fips)
            values.append(county["death_per_100"])

    df = pd.DataFrame({
        "county": counties,
        "value": values
    })

    df["county"] = df["county"].apply(clean_county_name)

    counties_geo["county"] = counties_geo["NAME"].apply(clean_county_name)

    merged = counties_geo.merge(
        df,
        on="county",
        how="left"
    )

    merged = merged[
        ~merged["STATEFP"].isin([
            "02", "15", "60", "66", "69", "72", "78"
        ])
    ]

    fig, ax = plt.subplots(figsize=(15, 10))

    merged.plot(
        column="value",
        cmap="viridis",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        },
        ax=ax,
        norm=LogNorm(
            vmin=1,
            vmax=merged["value"].max()
        ),
    )

    cbar = ax.get_figure().axes[-1]

    cbar.yaxis.set_major_formatter(ScalarFormatter())
    cbar.yaxis.set_major_locator(LogLocator(base=10))
    cbar.ticklabel_format(axis="y", style="plain")

    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)

    ax.set_title("Deaths by County per 100k")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "export/overall_county_deaths_per_100_map.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_state_death_per_100_map():
    states = []
    values = []
    for item in data:
        states.append(item["name"])
        values.append(item["death_per_100"])

    df = pd.DataFrame({
        "state": states,
        "value": values
    })

    merged = states_geo.merge(
        df,
        left_on="NAME",
        right_on="state",
        how="left"
    )

    merged = merged[
        ~merged["STUSPS"].isin([
            "AK", "HI", "PR", "AS", "GU", "MP", "VI"
        ])
    ]

    fig, ax = plt.subplots(figsize=(15, 10))

    merged.plot(
        column="value",
        cmap="viridis",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        },
        ax=ax,
        norm=LogNorm(
            vmin=1,
            vmax=merged["value"].max()
        ),
    )

    cbar = ax.get_figure().axes[-1]

    cbar.yaxis.set_major_formatter(ScalarFormatter())
    cbar.yaxis.set_major_locator(LogLocator(base=10))
    cbar.ticklabel_format(axis="y", style="plain")

    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)

    ax.set_title("Deaths by State per 100k")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "export/overall_state_deaths_per_100_map.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_state_death_map():
    states = []
    values = []
    for item in data:
        states.append(item["name"])
        values.append(item["overall_deaths"])

    df = pd.DataFrame({
        "state": states,
        "value": values
    })

    merged = states_geo.merge(
        df,
        left_on="NAME",
        right_on="state",
        how="left"
    )

    merged = merged[
        ~merged["STUSPS"].isin([
            "AK", "HI", "PR", "AS", "GU", "MP", "VI"
        ])
    ]

    fig, ax = plt.subplots(figsize=(15, 10))

    merged.plot(
        column="value",
        cmap="viridis",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        },
        ax=ax,
        norm=LogNorm(
            vmin=1,
            vmax=merged["value"].max()
        ),
    )

    cbar = ax.get_figure().axes[-1]

    cbar.yaxis.set_major_formatter(ScalarFormatter())
    cbar.yaxis.set_major_locator(LogLocator(base=10))
    cbar.ticklabel_format(axis="y", style="plain")

    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)

    ax.set_title("Deaths by State")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "export/overall_state_deaths_map.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_county_death_map():
    counties = []
    state_fips = []
    values = []

    for item in data:
        state = states_geo[
            states_geo["NAME"] == item["name"]
        ]

        if state.empty:
            continue

        fips = state.iloc[0]["STATEFP"]

        for county in item["counties"]:

            counties.append(clean_county_name(county["name"]))
            state_fips.append(fips)
            values.append(county["overall_deaths"])

    df = pd.DataFrame({
        "county": counties,
        "value": values
    })

    df["county"] = df["county"].apply(clean_county_name)

    counties_geo["county"] = counties_geo["NAME"].apply(clean_county_name)

    merged = counties_geo.merge(
        df,
        on="county",
        how="left"
    )

    merged = merged[
        ~merged["STATEFP"].isin([
            "02", "15", "60", "66", "69", "72", "78"
        ])
    ]

    fig, ax = plt.subplots(figsize=(15, 10))

    merged.plot(
        column="value",
        cmap="viridis",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        },
        ax=ax,
        norm=LogNorm(
            vmin=1,
            vmax=merged["value"].max()
        ),
    )

    cbar = ax.get_figure().axes[-1]

    cbar.yaxis.set_major_formatter(ScalarFormatter())
    cbar.yaxis.set_major_locator(LogLocator(base=10))
    cbar.ticklabel_format(axis="y", style="plain")

    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)

    ax.set_title("Deaths by County")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "export/overall_county_deaths_map.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_death_by_county_per_100(state_name: str):

    state = None

    for s in data:
        if s["name"] == state_name:
            state = s

    if state == None:
        return
    

    deaths = []

    counties = []

    for c in state["counties"]:
        deaths.append(c["death_per_100"])
        counties.append(c["name"])

    plt.figure(figsize=(10, 16))

    plt.barh(counties, deaths)
    plt.gca().invert_yaxis()

    plt.title(f"Deaths by County - {state_name}")
    plt.ylabel("County")
    plt.xlabel("Deaths per 100k")

    plt.tight_layout()

    os.makedirs(f"export/{state_name}", exist_ok=True)

    plt.savefig(
        f"export/{state_name}/deaths_by_county_per_100k.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_death_by_county(state_name: str):

    state = None

    for s in data:
        if s["name"] == state_name:
            state = s

    if state == None:
        return
    

    deaths = []

    counties = []

    for c in state["counties"]:
        deaths.append(c["overall_deaths"])
        counties.append(c["name"])

    plt.figure(figsize=(10, 16))

    plt.barh(counties, deaths)
    plt.gca().invert_yaxis()

    plt.title(f"Deaths by County - {state_name}")
    plt.ylabel("County")
    plt.xlabel("Number of Deaths")

    plt.tight_layout()

    os.makedirs(f"export/{state_name}", exist_ok=True)

    plt.savefig(
        f"export/{state_name}/deaths_by_county.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_death_by_intent(state_name: str, county_name: str):
    state = next(
        s for s in data
        if s["name"] == state_name
    )

    county = next(
        c for c in state["counties"]
        if c["name"] == county_name
    )

    intent_counts = {}

    for death in county["deaths"]:
        intent = death["intent"]
        count = death["deaths"]

        intent_counts[intent] = intent_counts.get(intent, 0) + count

    intents = list(intent_counts.keys())
    deaths = list(intent_counts.values())

    plt.figure(figsize=(10, 16))

    plt.barh(intents, deaths)
    plt.gca().invert_yaxis()

    plt.title(f"Deaths by Intent - {county_name}, {state_name}")
    plt.ylabel("Injury Intent")
    plt.xlabel("Number of Deaths")

    plt.tight_layout()
    os.makedirs(f"export/{state_name}/{county_name}", exist_ok=True)
    plt.savefig(
        f"export/{state_name}/{county_name}/deaths_by_intent.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_death_by_race(state_name: str, county_name: str):
    state = next(
        s for s in data
        if s["name"] == state_name
    )

    county = next(
        c for c in state["counties"]
        if c["name"] == county_name
    )

    intent_counts = {}

    for death in county["deaths"]:
        intent = death["race"]
        count = death["deaths"]

        intent_counts[intent] = intent_counts.get(intent, 0) + count

    intents = list(intent_counts.keys())
    deaths = list(intent_counts.values())

    plt.figure(figsize=(10, 16))

    plt.barh(intents, deaths)
    plt.gca().invert_yaxis()

    plt.title(f"Deaths by Intent - {county_name}, {state_name}")
    plt.ylabel("Race")
    plt.xlabel("Number of Deaths")

    plt.tight_layout()
    os.makedirs(f"export/{state_name}/{county_name}", exist_ok=True)
    plt.savefig(
        f"export/{state_name}/{county_name}/deaths_by_race.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_deaths_by_state():

    names = []
    deaths = []

    for item in data:
        names.append(item["name"])
        deaths.append(item["overall_deaths"])

    plt.figure(figsize=(10, 16))

    plt.barh(names, deaths)
    plt.gca().invert_yaxis()

    plt.title("Deaths by State")
    plt.ylabel("State")
    plt.xlabel("Number of Deaths")

    plt.tight_layout()
    plt.savefig(
        "export/overall_deaths.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

def graph_deaths_by_state_per_100():

    names = []
    deaths = []

    for item in data:
        names.append(item["name"])
        deaths.append(item["death_per_100"])

    plt.figure(figsize=(10, 16))

    plt.barh(names, deaths)
    plt.gca().invert_yaxis()

    plt.title("Deaths by State")
    plt.ylabel("State")
    plt.xlabel("Death per 100k")

    plt.tight_layout()
    plt.savefig(
        "export/overall_deaths_per_100.png",
        dpi=1200,
        bbox_inches="tight"
    )

    plt.close()

total = 6
for state in data:
    total += 1
    for county in state["counties"]:
        total += 1

cur = 0

graph_deaths_by_state()
cur += 1
progress_bar(cur, total)


graph_deaths_by_state_per_100()
cur += 1
progress_bar(cur, total)


graph_state_death_map()
cur += 1
progress_bar(cur, total)


graph_county_death_map()
cur += 1
progress_bar(cur, total)


graph_state_death_per_100_map()
cur += 1
progress_bar(cur, total)


graph_county_death_per_100_map()
cur += 1
progress_bar(cur, total)


for state in data:
    for county in state["counties"]:
        graph_death_by_intent(state["name"], county["name"])
        graph_death_by_race(state["name"], county["name"])
        cur += 1
        progress_bar(cur, total)
    graph_death_by_county(state["name"])
    graph_death_by_county_per_100(state["name"])
    cur += 1
    progress_bar(cur, total)