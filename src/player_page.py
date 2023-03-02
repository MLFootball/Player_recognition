from page import PagePath
import bs4
from collections import defaultdict

class AbstractPage:
    def __init__(self, pagepath: PagePath) -> None:
        self.pagepath = pagepath
        self._stats = defaultdict(str)
        self._naming_correspondence = {}
        self.soup = self._get_soup()

    def _get_soup(self):
        with open(str(self.pagepath)) as f:
            html_doc = f.read()
        return bs4.BeautifulSoup(html_doc, "html.parser")

    @property
    def stats(self):
        return self._stats

    def get_stats(self):
        raise NotImplementedError("To be written in inherited classes")


class TeamPage(AbstractPage):
    def __init__(self, pagepath: PagePath) -> None:
        super().__init__(pagepath)
    
    def get_stats(self):
        def cond(x):
            if x:
                return "odd" in x or "even" in x
            return False

        rows = self.soup.findAll('tr', {'class': cond})
        print(self.pagepath.curr_page_info, self.pagepath.page_date)
        # print(rows)
        for row in rows:
            team_shirts = [shirt.text for shirt in row.findAll("div", {"class": "tm-shirt-number"}) if shirt.text]
            player_names = [player.text for player in row.findAll("span", {"class": "hide-for-small"}) if player.text]
            for i in range(len(team_shirts)):
                self._stats[team_shirts[i]] = player_names[i]
        # print(self.stats)