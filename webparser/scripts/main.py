import os
import sys
from webparser.scripts import SoupParser

__author__ = 'hcao7'

BASE_DIR = os.path.dirname(__file__)


def run():
    html = os.path.join(BASE_DIR, 'cs473.html')
    link = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/spring/CS/373"

    scrape = SoupParser.Parser(html, 0, "test")
    # scrape = SoupParser.Parser(link, 1, "testURL")

if __name__ == "__main__":
    run()