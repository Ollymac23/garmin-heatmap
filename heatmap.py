#import gpxpy as gpx

from pathlib import Path
import pandas as pd
import gpxpy
import gpxpy.gpx
import csv
import plotly
import plotly.express as px

def createHeatmap(name):
    df = pd.read_csv(f"data/csvs/{name}.csv")

    fig = px.density_map(df, lat="latitude", lon="longitude", radius=4, center=dict(lat=52, lon=1), zoom=5, map_style="open-street-map")
    fig.show()
    




def createDataFile(dir):
    gpx_file = open(dir, "r")
    gpx = gpxpy.parse(gpx_file)
    name = str(dir).removeprefix("data\\gpxs\\")
    name = name.removesuffix(".gpx")

    points = []
    with open(f"data/csvs/{name}.csv", "w", newline="", encoding="utf-8") as csvactivity:
        csvwriter = csv.writer(csvactivity)
        csvwriter.writerow(["index", "latitude", "longitude", "elevation"])
        for track in gpx.tracks:

            for seg in track.segments:

                i = 0
                for point in seg.points:

                    if i % 1 == 0:

                        print(f"Point at ({point.longitude}, {point.latitude}) at elevation {point.elevation}")
                        csvwriter.writerow([i, point.latitude, point.longitude, point.elevation])
                    i += 1
    return name




def main():
    
    directory = Path("data/gpxs")


    files = [f for f in directory.iterdir() if f.is_file()]
    
    for i in range(len(files)):
        
        print(i, files[i])
    selected = int(input("which file would you like the data for: "))
    createHeatmap(createDataFile(files[selected]))


    


if __name__ == "__main__":
    main()