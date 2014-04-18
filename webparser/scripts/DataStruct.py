__author__ = 'hcao7'


class Course:
    def __init__(self, title, course, description):
        self.title = title
        self.course = course
        # self.credit
        self.description = description
        # self.prereq
        # self.misc
        # self.extra
        # self.sections
        # self.compelte


class Section:
    def __init__(self, crn, type, section, time, day, location, instructor, details):
        self.crn = crn
        self.type = type
        self.section = section
        self.time = time
        self.day = day
        self.location = location
        self.instructor = instructor
        self.details = details