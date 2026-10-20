#import gpxpy as gpx

from pathlib import Path
import pandas as pd
import gpxpy
import gpxpy.gpx
import csv
import plotly
import plotly.express as px
from nicegui import ui
import os

from createCSV import createWholeCSV as CCSV




def CreateHeatmap(name):

    df = pd.read_csv(f"data/csvs/{name}.csv")

    fig = px.density_map(df, lat="latitude", lon="longitude", radius=4, center=dict(lat=52, lon=1), zoom=5, map_style="open-street-map")
    return fig


def ShowHeatmap(name: str):
    fig = CreateHeatmap(name)
    plot_area.clear()
    with plot_area:
        ui.plotly(fig).classes("w-full h-[600px]")


ui.query("body").style("font-family: Helvetica, Arial, sans-serif")

with ui.row().style("display: flex; justify-content: center; width: 100%;"):
    ui.label("Garmin Heatmaps").style("color: #031B26; font-size: 40px; font-family: Arial, Helvetica, sans-serif; weight: bold;")


directory = Path("data/gpxs")


folders = [folder for folder in directory.iterdir() if folder.is_dir()]

with ui.column().style("width: 100%;"):
    with ui.row().classes("gap-2"):
        for folder in folders:
            ui.button(
                f"Create {folder.name}'s heatmap",
                on_click=lambda name=folder.name:ShowHeatmap(name),
                
            ).classes("w-64").style(
                "background-color: #AECE64 !important; "
                "color: #031B26 !important; border-radius: 12px; font-family:Helvetica;"
            )

    plot_area = ui.row().classes("flex-grow")

    


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Garmin Heatmap", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=False, show=False)
    