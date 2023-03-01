import os
FILENAME_DATE_SEP = "№"

class PagePath:
    def __init__(self, path) -> None:
        self._path = path
        filename = os.path.splitext(path.split(os.path.sep)[-1])[0]

        #_ join just in case if FILENAME_DATE_SEP is underscore _
        self._curr_page_info, self._page_date= "_".join(filename.split(FILENAME_DATE_SEP)[:-1]), filename.split(FILENAME_DATE_SEP)[-1]

        
    def __str__(self):
        return self._path

    @property
    def curr_page_info(self):
        return self._curr_page_info


    @property
    def page_date(self):
        return self._page_date
