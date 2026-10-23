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

uploadDir = Path("data/gpxs")

def FolderCheck():
    folderName = str(personName.value or "").lower()
    folderPath = Path(f"data/gpxs/{folderName}")
    dataPath = Path("data/gpxs")
    folders = [folder.name for folder in dataPath.iterdir() if folder.is_dir()]
    if folderName in folders:
        return folderName
    elif folderName == "" or None:
        return False
    else:
        os.makedirs(f"data/gpxs/{folderName}", exist_ok=True)
        return folderName

    


async def UploadHandler(e):

    folderName = FolderCheck()
    if folderName == False:
        ui.notify("Please enter a name", type="warning")
        return
    
    filename = Path(e.file.name).name
    target =  uploadDir / folderName / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(await e.file.read())
    ui.notify(f"Uploaded {filename} successfully.", type="positive")
    DrawFileList.refresh()

async def ConfirmDelete():
    with ui.dialog() as dialog, ui.card():
        ui.label("Are you sure you want to delete this folder and all its contents?")
        with ui.row():
            ui.button("Delete", on_click=lambda: dialog.submit(True)).style("background-color: red !important; color: #fdedee !important;")
            ui.button("Cancel", on_click=lambda: dialog.submit(False)).style("background-color: green !important; color: #fdedee !important")
    result = await dialog
    return result
            

def DeleteFolder(folder):



    pass

@ui.refreshable
def DrawFileList(folder):
    with ui.list().props("dense seperator").style("width: 100%; background-color: #454A5F !important; border-radius: 12px;"):

        dir = Path(folder)

        files = [file for file in dir.iterdir() if file.is_file()]
        for file in files:

            ui.item(
                file.name
            ).style("font-family: Impact, fantasy; color: #FDEDEE !important; font-size: 15;")

@ui.refreshable
def DrawButtons(folder):
    with ui.row():
        ui.button(
            f"Create {folder.name}'s heatmap",
            on_click=lambda name=folder.name:ShowHeatmap(CCSV(name)),
                        
        ).style(
            "background-color: #C62F4F !important; "
            "color: #FDEDEE !important; border-radius: 12px; font-family:Impact, fantasy; weight: bold; font-size: 20px;"
        )
        ui.button(
            icon="delete",
            on_click=lambda name=folder.name:DeleteFolder(name),
        ).style("background-color: #A60F2F !important; color: #fdedee !important; border-radius: 12px;")




    



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

ui.add_css("""
.name-input .q-field__control {
    background-color: #C62F4F !important;
    border-radius: 12px !important;
}

.name-input .q-field__control {
    color: #FDEDEE !important;
    font-family: Impact, fantasy;
}

.name-input .q-field--focused .q-field__control:after {
    border-color: #fdedee !important;
}

.gpx-upload {
    background-color: #C62F4F !important;
    border-radius: 12px !important;
    border-color: #000000;
}

.gpx-upload .q-uploader__header {
    background-color: #A60F2F !important;
    border-radius: 12px 12px 0 0;
    font-family: Impact, fantasy;
    font-weight: light !important;
}

.gpx-upload .q-uploader__subtitle,
.gpx-upload .q-uploader__title {
    color: #fdedee !important;
    font-weight: light !important;
}

.gpx-upload .q-uploader__list {
    background-color: #C62F4F !important;
    color: FDEDEE;
    min-height: 80px;
}

.gpx-upload .q-uploader__file {
    border-radius: 8px;
}



""")


with ui.row().style("display: flex; justify-content: center; width: 100%; background-color: #fdedee"):
    ui.label("Garmin Heatmaps").style("color: #011410; font-size: 40px; font-family: Impact, fantasy; weight: bold;")


directory = Path("data/gpxs")


folders = [folder for folder in directory.iterdir() if folder.is_dir()]

with ui.column().style("width: 100%;"):
    with ui.row().classes("gap-2").style("width: 100%; justify-content: center;"):
        for folder in folders:
            with ui.column().style("justify-content: center; padding: 15px;"):
                DrawButtons(folder)
                DrawFileList(folder)
    with ui.row().style("width: 100%; justify-content: center;"):
        with ui.column().style("align-content: center;"):
            personName = ui.input("Enter your name").props(
                "outlined rounded dense"
                ).classes("name-input").style("width: 100%;")
            ui.upload(
                label="Drop GPX files here",
                on_upload=UploadHandler,
                multiple=True,
                auto_upload=True,
                on_rejected=ui.notify("Upload failed.", type="negative")

            ).props("accept=.gpx").classes("gpx-upload")








    plot_area = ui.row().classes("flex-grow").style("justify-content: center;")


    


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Garmin Heatmap", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=False, show=False)
    