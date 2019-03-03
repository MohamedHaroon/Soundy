from os import path
import tqdm
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
        self.saving_directory = saving_directory
        self.html = requests.get(test_url, allow_redirects=False)
        self.soup = BeautifulSoup(self.html.content, 'html.parser')
        self.title = self.clean_title()
        self.track_id = self.get_id()
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

        forbidden_chars = ['<', '>', ':', '"', '/', '\\', '?', '*', '|']
        title = self.soup.title.string[:-31]
        # i can't find a way to assign the last loop variable to the last value so i create a list and add the cleaned up titles
        # and take the last one in the list and return it!
        # TODO: find a better way to clean it up!
        titles = []
        for i in forbidden_chars:
            if i in title:
                titles.append(title.replace(i,''))
        return(titles[-1])

    def get_id(self):
        '''

        Get the track ID which is used in Downloading the track
        '''

        #if false than it's unvalid SC track URL
        return re.search(r'soundcloud://sounds:(.+?)"', self.html.text).group(1)
        
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
        track_path = os.path.join(self.saving_directory, self.title + self.audio_format)
        with open(track_path, 'wb') as f:
            direct_request = requests.get(self.direct_link, stream=True)
            total_size = int(direct_request.headers['content-length'])
            for data in tqdm(iterable = direct_request.iter_content(chunk_size = 1024), total = total_size/1024, unit = 'KB'
            , desc = "Download Progress"):
                if data:
                    f.write(data)
                    f.flush() 

       
# test_track = Track("https://soundcloud.com/nurmusicpage/nur-bas-ba7awel") 
# test_track.download_track()