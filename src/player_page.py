from page import PagePath


class AbstractPage:
    def __init__(self, pagepath: PagePath) -> None:
        self.pagepath = pagepath
        self._stats = {}
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

