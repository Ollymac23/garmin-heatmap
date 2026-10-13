#import gpxpy as gpx

from pathlib import Path
import pandas as pd
import gpxpy
import gpxpy.gpx




def createDataFile(dir):
    gpx_file = open(dir, "r")
    gpx = gpxpy.parse(gpx_file)

    points = []
    for track in gpx.tracks:
        for seg in track.segments:
            for point in seg.points:
                print(f"Point at ({point.longitude}, {point.latitude}) at elevation {point.elevation}")



def main():
    
    directory = Path("data")


    files = [f for f in directory.iterdir() if f.is_file()]

    for file in files:
        print(file)
    selected = input("which file would you like the data for: ")
    if selected in files:
        createDataFile(selected)


    


if __name__ == "__main__":
    main()