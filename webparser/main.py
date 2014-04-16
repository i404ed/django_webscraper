#!/usr/bin/python
import sys
import requests


__author__ = 'hcao7'
import SoupParser


def main():
    html = "cs398.html"
    link = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/spring/CS/473"
    # link2 = "https://my.illinois.edu/uPortal/render.userLayoutRootNode.uP?uP_sparam=activeTabTag&activeTabTag=Academics&uP_fname=illinois-ssdt-courseinformationsuite&pltp_action=classView&pltp_year=2014&pltp_term=spring&pltp_course=CS&pltp_classNumber=398"
    # print requests.get(link)
    # print requests.get(link2)
    # sys.exit(0)

    scrape = SoupParser.Parser(html, 0, "test")
    # scrape = SoupParser.Parser(link, 1, "testURL")

    # scrape.get_links()
    # scrape.get_course()
    # scrape.get_text("CS 411")
    # scrape.print_data()
    # scrape.print_text()

if __name__ == "__main__":
    main()