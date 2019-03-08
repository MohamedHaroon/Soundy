import os
import argparse
from soundy import soundy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type = str, help = "Enter the track URL that you want to download."
                        , default = "https://soundcloud.com/basem98/anemone")
    parser.add_argument('--path', type = str, help = "Enter the path where the track will be downloaded."
                        , default = os.getcwd())
    args = parser.parse_args()
    try:
        # make an instace of Track
        track = soundy.Track(args.url, args.path)
        track.download_track()
    except Exception as e:
        return e 

if __name__ == "__main__":
    main()        