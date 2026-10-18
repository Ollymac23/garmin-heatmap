#import gpxpy as gpx

from pathlib import Path
import pandas as pd
import gpxpy
import gpxpy.gpx
import csv
import plotly
import plotly.express as px
from tkinter import *
from tkinter import ttk

from createCSV import createWholeCSV as CCSV


def createHeatmap(name):
    df = pd.read_csv(f"data/csvs/{name}.csv")

    fig = px.density_map(df, lat="latitude", lon="longitude", radius=4, center=dict(lat=52, lon=1), zoom=5, map_style="open-street-map")
    fig.show()
    



root = Tk()


def main():
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Garmin Heatmap").grid(column=0, row=0)
    

    directory = Path("data/gpxs")


    folders = [folder for folder in directory.iterdir() if folder.is_dir()]
    
    for i in range(len(folders)):
        ttk.Button(frm, text=f"Create {folders[i].name}'s heatmap", command=createHeatmap(CCSV(folders[i]))).grid(column=i, row=1)

    #NPTHING ELSE BELOW THIS IN MAIN
    Tk.mainloop(self=frm)




if __name__ == "__main__":
    main()
    