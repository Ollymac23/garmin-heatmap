import gpxpy
import csv
from pathlib import Path
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


def createWholeCSV(dir):
    with open(f"data/csvs/{dir.name}.csv", "w", newline="", encoding="utf-8") as mastercsv:
        csvwriter = csv.writer(mastercsv)
        #create table column headers
        csvwriter.writerow(["index", "latitude", "longitude", "elevation"])
        #populate table
        directory = Path(dir)
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
    return dir.name