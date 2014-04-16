__author__ = 'hcao7'
import re
import sys
from itertools import izip
import os
import errno
import urllib2

from bs4 import BeautifulSoup

import DataStruct
import models

BASE_DIR = os.path.dirname(__file__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# noinspection PyBroadException
class Parser:
    def __init__(self, src, mode, des):
        if mode == 0:
            f = open(src, 'r')
            self.soup = BeautifulSoup(f.read())
            f.close()
        elif mode == 1:
            data = urllib2.urlopen(src).read()
            # r = requests.get(src)
            # data = r.text
            self.soup = BeautifulSoup(data)
        else:
            print "mode has to be a .html file or a URL"

        self.print_pretty(des)
        self.get_course(des)

    def print_pretty(self, file_name):
        """
        pretty prints the html as (name)_pretty.html
        :param file_name: name
        """
        path = os.path.join(BASE_DIR, '../test/pretty_html')
        mkdir_p(path)
        orig_stdout = sys.stdout
        new_file = os.path.join(path, file_name + "_pretty.html")
        f = open(new_file, 'w')
        sys.stdout = f
        print(self.soup.prettify().encode('utf-8'))
        sys.stdout = orig_stdout
        f.close()
        f = open(new_file, 'r')
        self.soup = BeautifulSoup(f.read())
        f.close()

    def get_course(self, file_name):
        """
        prases the html and save to file as (name)_parsed.txt
        :param file_name: name
        """
        path = os.path.join(BASE_DIR, '../test/parsed_txt')
        mkdir_p(path)
        orig_stdout = sys.stdout
        new_file = os.path.join(path, file_name + "_parsed.txt")
        f = open(new_file, 'w')
        sys.stdout = f

        root = self.soup.find("div", class_="portlet-content-inner")

        # course title, course name, credit hrs, description, same as, prereqs
        try:
            # course title
            title = root.find("p", class_="cis-section-title")
            title_text = title.get_text(strip=True).encode('utf-8')
            # print title_text
            # print title[0].contents[0].strip().encode('utf-8')

            # course name
            try:
                course = root.find("p", class_="cis-section-course")
                course_text = course.get_text(strip=True).encode('utf-8')
                # print course_text
                # print course[0].contents[0].strip().encode('utf-8')
            except:
                course_text = "Course Name Not Found"
                # print course_text
                pass

            # hours, description, prereqs, same as
            try:
                subject_infos = root.find_all("div", id=re.compile("^subject-info"))
                descendants = subject_infos[0].find_all("p", class_="portlet-padtop10")
                credit_hr = descendants[0]
                credit_hr_text = credit_hr.get_text(" ", strip=True).encode('utf-8')
                # print credit_hr_text
                # print credit_hr.contents[1].contents[0].strip().encode('utf-8')
                # print credit_hr.contents[2].strip().encode('utf-8')
                description = descendants[1]
                description_text = description.get_text(strip=True).encode('utf-8') + " "
                # print "Description: " + description_text
                # print descript.contents[0].strip().encode('utf-8')

                # template is sort of messed up. 373 vs 125 + 473
                # descendants 2 doesnt exist?
                # sometimes prereq is build into description
                # sometimes, prereqs and etc are in here. if they are not in here, they are in crosslink
                try:
                    prereq = descendants[2]
                    prereq_text = prereq.get_text(strip=True).encode('utf-8') + " "
                    # print prereq_text
                    # print prereq.contents[0].strip().encode('utf-8')
                except:
                    prereq_text = ""
                    pass
                    # print "Prereqs Not Found"

                # sometimes, Same as and prereqs are in this tag instead
                try:
                    cross_link = root.find_all("div", id=re.compile("^schedule-crosslink"))
                    cross = cross_link[0]
                    cross_text = cross.get_text(strip=True).encode('utf-8') + " "
                    # print cross_text
                except:
                    cross_text = ""
                    pass
                    # print "Crosslink Not Found"

                # cs 373's 'Students must register for one lecture and one discussion section.'
                try:
                    misc = subject_infos[1].find_all("p", class_="portlet-padtop10")
                    misc_text = misc.get_text(strip=True).encode('utf-8') + " "
                    # print misc_text
                    # print misc[0].contents[0].strip().encode('utf-8')
                except:
                    misc_text = ""
                    pass
                    # print "Misc Not Found"

                # finds the next sibling if it exists
                # This course satisfies the General Education Criteria in SPRING 2014 for a
                # UIUC: Quant Reasoning II course
                try:
                    extra = subject_infos[0].find_next_sibling("p", class_="portlet-padtop10")
                    extra_text = extra.get_text(" ", strip=True).encode('utf-8')
                    # print extra_text
                    # print extra.contents[1].contents[0].strip().encode('utf-8')
                    # print extra.contents[1].contents[1].contents[0].strip().encode('utf-8')
                    # print extra.contents[4].strip().encode('utf-8')
                except:
                    extra_text = ""
                    pass
                    # print "Extra Not Found"
                description_text = description_text + prereq_text + cross_text + misc_text + extra_text
            # hours, description, prereqs, same as
            except:
                credit_hr_text = "Credit Hours Not Found"
                description_text = "Description Not Found"
                pass

            prereq_start = description_text.find("Prerequisite: ")
            if prereq_start != -1:
                prereq_end = description_text.find(".", prereq_start + 1)
                find_prereq = description_text[prereq_start:prereq_end + 1]
            else:
                prereq_end = prereq_start
                find_prereq = "Prerequisite Not Found"
            # print prereq_start, prereq_end, find_prereq
            sameas_start = description_text.find("Same as")
            if sameas_start != -1:
                sameas_end = description_text.find(".", sameas_start + 1)
                find_sameas = description_text[sameas_start:sameas_end + 1]
            else:
                sameas_end = sameas_start
                find_sameas = "Same As Not Found"
            # print sameas_start, sameas_end, find_sameas


            # all_entries = models.Course.objects.all()
            course_obj = DataStruct.Course(title_text, course_text, description_text)
            # course_model, course_bool = models.Course.objects.get_or_create(
            #     CourseID=title_text, CourseName=course_text, Description=description_text)

            print course_obj.title
            print course_obj.course
            # print title_text
            # print course_text
            print credit_hr_text
            print course_obj.description
            # print description_text
            print find_prereq
            print find_sameas

        except:
            pass
            # print "Course Not Found"

        # the schedule
        # only crn is guaranteed to be single
        try:
            table_struct = subject_infos[0].find_next_sibling("div", class_="portlet-container-flex")
            table = table_struct.find("tbody")
            # (table-item[^ ]*) ([^ ]+) (.*)
            # doesnt match on space?
            table_entry = table.find_all("tr", class_=re.compile(r"^table-item$"))
            table_entry_info = table.find_all("tr", class_=re.compile(r"^table-item-detail"))
            assert len(table_entry) == len(table_entry_info)
            # length of the 2 should be the same
            # begin deciphering
            for entry, info in izip(table_entry, table_entry_info):
                w50 = entry.find_all("td", class_="w50")
                w80 = entry.find_all("td", class_="w80")
                w55 = entry.find_all("td", class_="w55")
                w75 = entry.find_all("td", class_="w75")
                w120 = entry.find_all("td", class_="w120")
                ie_table_width = entry.find_all("td", class_=re.compile(r"ie-table-width"))

                icon0 = w50[0]
                crn = w50[1]
                crn_text = crn.get_text(strip=True).encode('utf-8')
                # print "CRN: " + crn_text
                # print "CRN: " + crn.contents[1].contents[0].strip().encode('utf-8')

                types = w80[0]
                section = w55[0]
                time = w75[0]
                days = w55[1]
                location = w120[0]
                instructors = ie_table_width[0]

                type_text = types.get_text("\n", strip=True).encode('utf-8')
                section_text = section.get_text("\n", strip=True).encode('utf-8')
                time_text = time.get_text("\n", strip=True).encode('utf-8')
                day_text = days.get_text("\n", strip=True).encode('utf-8')
                location_text = location.get_text("\n", strip=True).encode('utf-8')
                instructor_text = instructors.get_text("\n", strip=True).encode('utf-8')

                # takes care of paired classes like cs398
                # types, sections, times, days, locations, teachers
                # try:
                #     for blocks in xrange(len(types)):
                #         if blocks % 2 == 0:
                #             print "Type: " + types.contents[blocks + 1].contents[0].strip().encode('utf-8')
                #             print "Section: " + section.contents[blocks + 2].strip().encode('utf-8')
                #             print "Time: " + time.contents[blocks + 1].contents[0].strip().encode('utf-8')
                #             print "Day: " + days.contents[blocks + 1].contents[0].strip().encode('utf-8')
                #             print "Location: " + location.contents[blocks + 1].contents[0].strip().encode('utf-8')
                #             # takes care of multiple teachers per row
                #             for n in xrange(len(instructors.contents[blocks + 1].contents)):
                #                 if n % 2 == 0:
                #                     try:
                #                         # ignore blank lines
                #                         if instructors.contents[1].contents[n].strip() != "":
                #                             print "Instructor: " + instructors.contents[1].contents[n].strip().encode(
                #                                 'utf-8')
                #                     except:
                #                         pass
                # except:
                #     pass

                # details always comes in pairs
                # Availability: Open
                # Section Title: Computer Architecture
                # Part of Term: 1
                # Section Info: Lab sections meets in 0218 Siebel Center
                details_list = info.find_all("div", class_="yui3-g")
                detail_text = ""
                for details in details_list:
                    detail_text += details.get_text(" ", strip=True).encode('utf-8') + "\n"
                    # print details.get_text(" | ", strip=True).encode('utf-8')
                    # print details.contents[1].contents[0].strip().encode('utf-8')
                    # print details.contents[3].contents[0].strip().encode('utf-8')
                # deciphering ends here

                section_obj = DataStruct.Section(crn_text, type_text, section_text, time_text, day_text, location_text,
                                                 instructor_text, detail_text)
                # section_model, section_bool = models.Slots.objects.get_or_create(
                #     CRN=crn_text, Type=type_text, Time=time_text, Section=section_text,
                #     Days=day_text, Location=location_text, Professor=instructor_text, CourseID=title_text)


                print "CRN: " + section_obj.crn
                print "Type: " + section_obj.type
                print "Section: " + section_obj.section
                print "Time: " + section_obj.time
                print "Day: " + section_obj.day
                print "Location: " + section_obj.location
                print "Instructor: " + section_obj.instructor
                # print "CRN: " + crn_text
                # print "Type: " + type_text
                # print "Section: " + section_text
                # print "Time: " + time_text
                # print "Day: " + day_text
                # print "Location: " + location_text
                # print "Instructor: " + instructor_text
                print detail_text

        except:
            pass
            # print "Course Sections Not Found"

        sys.stdout = orig_stdout
        f.close()

    # def get_links(self):
    #     orig_stdout = sys.stdout
    #     f = open('links.txt', 'w')
    #     sys.stdout = f
    #     for link in self.soup.find_all('a'):
    #         print(link.get('href'))
    #     sys.stdout = orig_stdout
    #     f.close()

    # def get_text(self, find):
    #     orig_stdout = sys.stdout
    #     f = open('text_find.txt', 'w')
    #     sys.stdout = f
    #     print self.soup.find_all(text=find)
    #     sys.stdout = orig_stdout
    #     f.close()

    # def print_data(self):
    #     orig_stdout = sys.stdout
    #     f = open('data.txt', 'w')
    #     sys.stdout = f
    #     print self.data
    #     sys.stdout = orig_stdout
    #     f.close()

    # def print_text(self):
    #     orig_stdout = sys.stdout
    #     f = open('text.txt', 'w')
    #     sys.stdout = f
    #     print self.soup.get_text().encode('utf-8')
    #     sys.stdout = orig_stdout
    #     f.close()