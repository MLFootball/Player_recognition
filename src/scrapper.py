
import requests
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from dateutil.relativedelta import relativedelta
import time
import json
import collections
import re
from page import PagePath


MAX_TIMER = 60

REFRESH_RATE = 14

FILENAME_DATE_SEP = "№"

class Player:
    def __init__(self, url: str, project_dir = ".", verbose=False, outname="") -> None:
        """
        Initial url obtained from google docs should be in form 
        https://www.hltv.org/player/3741/player_name
        """
        url_pattern = re.compile("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
        if not url_pattern.match(url):
            raise ValueError("Wrong url Error.")

        self.url = url
        self.player_name = ""
        if not os.path.isdir(project_dir):
            raise ValueError("Wrong project directory path: Not a directory")
        self.project_dir = project_dir
        self.verbose = verbose
        self.outname = outname
        self.url_dict = {}

        if not os.path.exists(self.project_dir):
            os.mkdir(self.project_dir)

        if not os.path.exists(f"{self.project_dir}{os.path.sep}data"):
            os.mkdir(f"{self.project_dir}{os.path.sep}data")
        player_path = f"{self.project_dir}{os.path.sep}data{os.path.sep}{self.player_name}"
        if not os.path.exists(player_path):
            os.mkdir(player_path)
        
        self._get_urls()
        
        self.pages = []
        


        self._page_correspondence = {
        }

        
        
    
    def _get_urls(self):
        raise NotImplementedError("")

       


    def to_refresh(self, tag):
        """
        Check whether player's directory exists and decide whether to parse data from url
        if difference between current date and latest cached result if larger than refresh rate
        """
        raise NotImplementedError("")



    def save_html(self, url, tag, timer=1):
        
        if not self.to_refresh(tag):
            return
        
        curr_date = date.today()

        try:
            time.sleep(timer)
            stats = requests.get(url)
        except requests.exceptions.Timeout:
            if timer > MAX_TIMER:
                if not os.path.exists(f"{self.project_dir}{os.path.sep}log"):
                    os.mkdir(f"{self.project_dir}{os.path.sep}log")
                with open(f"{self.project_dir}{os.path.sep}log{os.path.sep}{self.player_name}_{tag}_{curr_date}.txt", mode = "w") as f:
                    f.write(f"Player {self.player_name} stats by url {url} couldnt be obtained after waiting more than the threshold of {MAX_TIMER} seconds.")
                return
            self.save_html(self.player_name, url, timer=timer * 2)
        except requests.exceptions.TooManyRedirects:
            with open(f"{self.project_dir}{os.path.sep}log{os.path.sep}{self.player_name}_{tag}_{curr_date}.txt", mode = "w") as f:
                    f.write(f"Player {self.player_name} stats by url {url} couldnt be obtained because of too many redirects.")
        except requests.exceptions.RequestException as e:
            with open(f"{self.project_dir}{os.path.sep}log/{self.player_name}_{tag}_{curr_date}.txt", mode = "w") as f:
                    f.write(f"Player {self.player_name} stats by url {url} couldnt be obtained because of some error {e}")
        
        

        html_text = stats.text
        with open(f"{self.project_dir}{os.path.sep}data{os.path.sep}{self.player_name}/{tag}{FILENAME_DATE_SEP}{curr_date}.html", mode="w") as f:
            f.write(html_text)

    def update_pages(self):
        raise NotImplementedError("")

    def cache_all_pages(self):
        for tag, url in self.url_dict.items():
            if self.verbose:
                print(f"Processing {tag}")
            self.save_html(url, tag)
        
        self.update_pages()




    def get_stats(self):
        all_stats = {}

        num_page = 1

        for page in self.pages:
            if self.verbose:
                print(f"\nScrapping. Current page: {page.curr_page_info}. Page number: {num_page}")
            num_page += 1
            curr_page = self._page_correspondence[page.stat](page)
            curr_page.get_stats()
            all_stats.update(curr_page.stats)
        return all_stats
        
    def save_stats(self, all_stats):
        if not self.outname:
            self.outname = f"{self.player_name}_stats_{date.today()}.json"
        else:
            if not os.path.splitext(self.outname)[0]:
                self.outname += ".json"
        results_dir = f"{self.project_dir}{os.path.sep}results"
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        
        od = collections.OrderedDict(sorted(all_stats.items()))
        if self.verbose:
            print(f"Saving stats to {results_dir}{os.path.sep}{self.outname}")
        with open(f"{results_dir}{os.path.sep}{self.outname}", mode="w") as f:
            json.dump(od, f)
    