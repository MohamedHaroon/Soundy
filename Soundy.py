from os import path
import os
import argparse
import sys
import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


class Track:
    audio_format = ".mp3"

    def __init__(self,test_url, saving_directory = os.getcwd()):
        '''

        Initialize the saving directory( The same directory of the script by default )
        And checks if the URL is a valid SoundCloud track 
        '''
        self.saving_directory = saving_directory
        self.url = test_url
        self.check_track()
        self.track_id = self.get_id()
        self.title = self.clean_title()
        self.direct_link = self.download_link()

    
    def clean_title(self):
        r'''

        Cleans the title from forbidden chars that will raise an error if used in a file on windows 
        so it iterates over them to check if any exists inside the title and then removes them
                < (less than)
                > (greater than)
                : (colon)
                " (double quote)
                / (forward slash)
                \ (backslash)
                | (vertical bar or pipe)
                ? (question mark)
                * (asterisk)
        '''  
        # TODO: find a better way to clean it up!
        # appends the title to a list and every time a forbidden char comes up it removes it and appends the clean
        # -version of it to the list and so on untill there is no forbidden chars in the title
        # returns the last item of the list -cleaned up title-
        # if doesn't contain any forbidden chars return the title as it is as it's the only item in the list
        forbidden_chars = ['<', '>', ':', '"', '/', '\\', '?', '*', '|']
        title = self.soup.title.string[:-31]
        titles = []
        titles.append(title)
        for title in titles:
            for char in forbidden_chars:
                if char in title:
                    print("Title got A symbol that will ruin your download...cleaning them up for you wait a second!")
                    titles.append(titles[-1].replace(char ,'')) 
        return(titles[-1])

    def get_id(self):
        '''

        Get the track ID which is used in Downloading the track
        '''
        #if false than it's unvalid SC track URL
        try:
            return re.search(r'soundcloud://sounds:(.+?)"', self.html.text).group(1)
        except AttributeError:
            print("Invalid SoundCloud track check your connection and/or if you have access to the track!")

        
    def download_link(self) :
        '''

        Extracts the direct download URL
        '''

        final_page = requests.get(
            f"https://api.soundcloud.com/i1/tracks/{self.track_id}/streams?client_id=Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0"
            )              
        return final_page.json()['http_mp3_128_url']
   
    def download_track(self):
        '''
        
        Uses the download URL to download the track to the choosen directory
        '''
        print("Downloading started!!")
        track_path = os.path.join(self.saving_directory, self.title + self.audio_format)
        try:
            with open(track_path, 'wb') as f:
                direct_request = requests.get(self.direct_link, stream=True)
                total_size = int(direct_request.headers['content-length'])
                for data in tqdm(iterable = direct_request.iter_content(chunk_size = 1024), total = total_size/1024, unit = 'KB'
                , desc = "Download Progress"):
                    if data:
                        f.write(data)
                        f.flush()
            print("Download complete.")            
        except OSError:
            print("Invalid given directory, will try to download to the current directory")
            self.title =  self.clean_title()
            self.saving_directory = os.getcwd()
            self.download_track()                 
        
# test_url = "https://soundcloud.com/mazagangy1/sayad"
# test_track = Track(test_url) 
# test_track.download_track()