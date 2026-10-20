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

uploadDir = Path("data/gpxs/olly")

async def UploadHandler(e):
    filename = Path(e.file.name).name
    target = uploadDir / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(e.file.read())
    ui.notify(f"Uploaded {e.name} successfully.")


def CreateHeatmap(name):

    CCSV(name)

    

    df = pd.read_csv(f"data/csvs/{name}.csv")

    fig = px.density_map(df, lat="latitude", lon="longitude", radius=4, center=dict(lat=52, lon=1), zoom=5, map_style="open-street-map")
    return fig


def ShowHeatmap(name: str):
    fig = CreateHeatmap(name)
    plot_area.clear()
    with plot_area:
        ui.plotly(fig).classes("w-full h-[600px]")
        ui.label("Look around the map to see where you've been the most!").style("font-family: Impact, fantasy; font-size: 30px; color: #EBF9DC;")


ui.query("body").style("font-family: Helvetica, Arial, sans-serif; background-color: #333747")

with ui.row().style("display: flex; justify-content: center; width: 100%; background-color: #EBF9DC"):
    ui.label("Garmin Heatmaps").style("color: #011410; font-size: 40px; font-family: Impact, fantasy; weight: bold;")


directory = Path("data/gpxs")


folders = [folder for folder in directory.iterdir() if folder.is_dir()]

with ui.column().style("width: 100%;"):
    with ui.row().classes("gap-2").style("width: 100%; justify-content: center;"):
        for folder in folders:
            with ui.column().style("justify-content: center;"):
                ui.button(
                    f"Create {folder.name}'s heatmap",
                    on_click=lambda name=folder.name:ShowHeatmap(CCSV(name)),
                    
                ).style(
                    "background-color: #C62F4F !important; "
                    "color: #FDEDEE !important; border-radius: 12px; font-family:Impact, fantasy; weight: bold; font-size: 20px;"
                )

                ui.upload(
                    label="Drop GPX files here",
                    on_upload=UploadHandler,
                    multiple=True,
                    auto_upload=True,
                    on_rejected=ui.notify("Upload failed.", type="negative")

                ).props("accept=.gpx")


                directory = Path(folder)
                files = [file for file in directory.iterdir() if folder.is_dir()]


                with ui.list().props("dense").style("width: 100%; background-color: #454A5F !important; border-radius: 12px;"):

                    for file in files:

                        ui.item(file.name).style("font-family: Impact, fantasy; background color: #454A5F !important; color: #EBF9DC;")


    plot_area = ui.row().classes("flex-grow").style("justify-content: center;")


    


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Garmin Heatmap", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=False, show=False)
    