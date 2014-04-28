import os
import sys
from webparser.scripts import SoupParser
from webparser.scripts import DeptParser

__author__ = 'hcao7'

BASE_DIR = os.path.dirname(__file__)


# https://courses.illinois.edu/cisapp/dispatcher/catalog/2014/fall/ACE
# https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/fall/ACE/231
def run():
    html = os.path.join(BASE_DIR, 'base_html/cs398.html')
    link = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/fall/CS/398"
    # SoupParser.Parser(html, 0, "test")
    # SoupParser.Parser(link, 1, "testURL")


    dept_link = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/fall/ARTD"
    DeptParser.Dept(dept_link, 1, "a")

if __name__ == "__main__":
    run()