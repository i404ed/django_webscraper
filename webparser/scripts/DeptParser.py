import sys
from webparser.scripts import SoupParser

__author__ = 'hcao7'

import urllib2
from bs4 import BeautifulSoup

BASE_URL = "https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/fall/"
# https://courses.illinois.edu/cisapp/dispatcher/catalog/2014/spring/ACE
# https://courses.illinois.edu/cisapp/dispatcher/schedule/2014/fall/ACE/100


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


class Dept:
    def __init__(self, src, mode, des):
        if mode == 0:
            print "Does nothing"
            # f = open(src, 'r')
            # self.soup = BeautifulSoup(f.read(), "lxml")
            # f.close()
        elif mode == 1:
            data = urllib2.urlopen(src).read()
            # r = requests.get(src)
            # data = r.text
            self.soup = BeautifulSoup(data, "lxml")
        else:
            print "mode has to be a .html file or a URL"

        self.get_course_list(des)

    def get_course_list(self, des):
        print "Grabbing list of Courses:"
        root = self.soup.find("tbody")
        course_list = root.find_all("tr")
        print "Grabbing list of Courses:COMPLETED"
        for course in course_list:
            course_text = course.get_text("/", strip=True).encode('utf-8')
            course_link = course_text[:find_nth(course_text, "/", 2)]
            print course_link
            SoupParser.Parser(BASE_URL + course_link, 1, "testURL")