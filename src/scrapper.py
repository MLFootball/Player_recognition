
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
from player_page import TeamPage
from collections import defaultdict
import bs4


MAX_TIMER = 60

REFRESH_RATE = 14

FILENAME_DATE_SEP = "№"

class Player:
    def __init__(self, url: str, player_name: str = "team", project_dir = ".", verbose=False, outname="") -> None:
        """
        Initial url obtained from google docs should be in form 
        https://www.hltv.org/player/3741/player_name
        """
        url_pattern = re.compile("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
        if not url_pattern.match(url):
            raise ValueError("Wrong url Error.")

        self.url = url
        self.player_name = player_name
        if not os.path.isdir(project_dir):
            raise ValueError("Wrong project directory path: Not a directory")
        self.project_dir = project_dir
        self.verbose = verbose
        self.outname = outname
        self.url_dict = defaultdict(str)

        if not os.path.exists(self.project_dir):
            os.mkdir(self.project_dir)

        if not os.path.exists(f"{self.project_dir}{os.path.sep}data"):
            os.mkdir(f"{self.project_dir}{os.path.sep}data")
        player_path = f"{self.project_dir}{os.path.sep}data{os.path.sep}{self.player_name}"
        if not os.path.exists(player_path):
            os.mkdir(player_path)
        
        self._get_urls()
        self.update_pages()

        
        self.pages = []
        


        self._page_correspondence = {
        }

        

    
    def _get_urls(self):
        # stats = requests.get(self.url, headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } )
        # html_text = stats.text
        # # print(html_text)
        # with open("br_leage.html", mode="w") as f:
        #     f.write(html_text)
        with open("br_leage.html", mode="r") as f:
            html_text = f.read()
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        # lst = [t for t in soup.find_all("tr") if not isinstance(t, bs4.element.NavigableString)]
        # # for elm in lst:
        # print(lst, len(lst))
        tds = []
        # soup = BeautifulSoup(page_src, 'html.parser')
        divs = soup.findAll("span", {"class": "vereinsname"})
        # print(set(divs))
        # print(divs)

        for span in divs:
            # print(div.contents)
            links = span.find_all('a')
            for link in links:
                if "saison" in link["href"]:
                    l = link['href'].replace("spielplan", "startseite")
                    self.url_dict[link.text] = f"https://www.transfermarkt.com{l}"
        pprint(self.url_dict)
        #     rows = div.findAll('tr')
        #     print(rows)
        #     for row in rows :
        #         tds.append(row.findAll('td'))
        # print(tds)
        # for tag in soup.find_all("td", {"class": "hauptlink no-border-links"}):
        #     for info in tag.contents:
                # if  isinstance(info, bs4.element.NavigableString):
                #     continue
                
                # print(info.text)
            
                # for key in self._stats.keys():
                #     if info.text.strip() in key and not info.text.strip().isdigit() :
                #         self._stats[f"{self.pagepath.curr_page_info}_{info.text.strip()}"] = stat_value
                #         continue

                # stat_value = info.text.strip()
                # if stat_value == "-":
                #     stat_value = "0"

       


    def to_refresh(self, tag):
        """
        Check whether player's directory exists and decide whether to parse data from url
        if difference between current date and latest cached result if larger than refresh rate
        """
        raise NotImplementedError("")



    def save_html(self, url, tag, timer=1):
        
        # if not self.to_refresh(tag):
        #     return
        
        curr_date = date.today()

        try:
            time.sleep(timer)
            stats = requests.get(url, headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' })
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
        player_path = f"{self.project_dir}{os.path.sep}data{os.path.sep}{self.player_name}"
        self.pages = [ pagefile for pagefile in os.listdir(player_path)]
        

        self.pages = [PagePath(f"{player_path}{os.path.sep}{pagefile}") for pagefile in self.pages]
        #sort pages by date
        self.pages = sorted(self.pages, reverse=True, key=lambda x: x.page_date)
        #get the most recent pages that are necessary for getting whole stat
        # self.pages = self.pages[:len(self.url_dict)]


    def cache_all_pages(self):
        for tag, url in self.url_dict.items():
            if self.verbose:
                print(f"Processing {tag}")
            self.save_html(url, tag)
        
        self.update_pages()




    def get_stats(self):
        all_stats = defaultdict(str)

        num_page = 1

        for page in self.pages:
            if self.verbose:
                print(f"\nScrapping. Current page: {page.curr_page_info}. Page number: {num_page}")
            num_page += 1
            curr_page = TeamPage(page)
            curr_page.get_stats()
            # print(curr_page.stats)
            all_stats[page.curr_page_info] = dict(curr_page.stats)
        return dict(all_stats)
        
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
        with open(f"{results_dir}{os.path.sep}{self.outname}", mode="w", encoding="utf-8") as f:
            json.dump(od, f)
    

if __name__ == "__main__":
    gb_pl = Player(url = "https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1", player_name="Laliga")
    # gb_pl.cache_all_pages()
    gb_pl.update_pages()
    print(gb_pl.pages)
    stats = gb_pl.get_stats()
    pprint(stats)
    gb_pl.save_stats(stats)
