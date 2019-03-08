# Soundy
A light-weight SoundCloud package to download and scrape tracks.

## Installation 
you can install Soundy from [PyPI](https://pypi.org/project/soundy/):

    pip install soundy

soundy is tested on python 3.7

## Usage 
Soundy is a command line application, You can download a specific track using the following command
       
    python -m soundy --url track-url-here --path path-here

the default download path is the directory which you run the command from 

You can also use Soundy in your own Python code, by importing from the `soundy` package:

    >>> from soundy import soundy as sd
    >>> track = sd.Track(url = "url", path = r"path")
    >>> track.download_track()

