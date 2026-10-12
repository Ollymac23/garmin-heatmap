#import gpxpy as gpx

from pathlib import Path








def main():
    
    directory = Path("data")


    files = [f for f in directory.iterdir() if f.is_file()]

    for file in files:
        print(file)
    input("which file would you like the data for: ")

if __name__ == "__main__":
    main()