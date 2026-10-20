import gpxpy
import csv
from pathlib import Path



def createWholeCSV(dir):
    with open(f"data/csvs/{dir}.csv", "w", newline="", encoding="utf-8") as mastercsv:
        csvwriter = csv.writer(mastercsv)
        #create table column headers
        csvwriter.writerow(["index", "latitude", "longitude", "elevation"])
        #populate table
        directory = Path(f"data/gpxs/{dir}")
        files = [file for file in directory.iterdir() if file.is_file()]
        for file in files:
            gpx_file = open(file, "r")
            gpx = gpxpy.parse(gpx_file)
            name = file.name

            points = []
            for track in gpx.tracks:
                for seg in track.segments:

                    i = 0
                    for point in seg.points:
                        if i % 1 == 0:
                            csvwriter.writerow([i, point.latitude, point.longitude, point.elevation])
                            i += 1
    return dir