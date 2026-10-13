#import gpxpy as gpx

from pathlib import Path
import pandas as pd
import gpxpy
import gpxpy.gpx
import csv



def createDataFile(dir):
    gpx_file = open(dir, "r")
    gpx = gpxpy.parse(gpx_file)

    points = []
    with open("/data/csvs/activity.csv", "w", newline="", encoding="utf-8") as csvactivity:
        for track in gpx.tracks:
            for seg in track.segments:
                
                for point in seg.points:
                    print(f"Point at ({point.longitude}, {point.latitude}) at elevation {point.elevation}")
                    csvwriter = csv.writer(csvactivity)
                    csvwriter.writerow([point.latitude, point.longitude, point.elevation])




def main():
    
    directory = Path("data/gpxs")


    files = [f for f in directory.iterdir() if f.is_file()]
    
    for i in range(len(files)):
        
        print(i, files[i])
    selected = int(input("which file would you like the data for: "))
    createDataFile(files[selected])


    


if __name__ == "__main__":
    main()