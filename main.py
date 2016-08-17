
'''
Author: Mustafa Camurli
Data: : 16.08.2016 (Tuesday)
E-mail: mustafa.camurli@gmail.com
'''

import re
import sys
import string

PROGRAM_NAME_STRING               = "Bilgisayar Mühendisliği"

PROGRAM_LANG_ENGLISH_STRING       = "(İngilizce)"
PROGRAM_LANG_GERMAN_STRING        = "(Almanca)"

PROGRAM_EVENING_EDU_STRING        = "(İÖ)"

PROGRAM_SCHOLARSHIP_MARKER_STRING = "Burslu"
PROGRAM_25_PER_SCHOLARSHIP_STRING = "%25 Burslu"
PROGRAM_50_PER_SCHOLARSHIP_STRING = "%50 Burslu"
PROGRAM_75_PER_SCHOLARSHIP_STRING = "%75 Burslu"
PROGRAM_NO_SCHOLARSHIP_STRING     = "Ücretli"
PROGRAM_FULL_SCHOLARSHIP_STRING   = "Tam Burslu"

PROGRAM_TECH_HIGH_SCHOOL_PRIV     = "(M.T.O.K.)"

PROGRAM_FIELD_MARKER_STRING       = "MF-4"

PROGRAM_SCORE_NONE_STRING         = "---"

class Language(enumerate):
    TURKISH = 1
    ENGLISH = 2
    GERMAN  = 3

class MalformedUniversityStringException(Exception):
    def __init__(self, str):
        Exception.__init__(self, "MalformedUniversityStringException")
        self.str = str

class MalformedFacultyStringException(Exception):
    def __init__(self, str):
        Exception.__init__(self, "MalformedFacultyStringException")
        self.str = str

class MalformedProgramStateStringException(Exception):
    def __init__(self, str):
        Exception.__init__(self, "MalformedProgramStateStringException")
        self.str = str

class Program:
    __name = None
    __language = None
    __scholarship = None
    __is_evening_edu = None
    __is_tech_high_school_priv = None
    __student_quota = None
    __num_of_student_got_in = None
    __score_lower_bound = None
    __score_upper_bound = None

    def __get_program_lang_from_string(self, program_str):
        if ( -1 != program_str.find(PROGRAM_LANG_ENGLISH_STRING) ):
            return (Language.ENGLISH)
        elif ( -1 != program_str.find(PROGRAM_LANG_GERMAN_STRING) ):
            return (Language.GERMAN)
        else:
            return (Language.TURKISH)

    def __get_program_is_evening_edu_state_from_string(self, program_str):
        if ( -1 != program_str.find(PROGRAM_EVENING_EDU_STRING) ):
            return (True)
        return (False)

    def __get_program_is_tech_high_school_priv_state_from_string(self, program_str):
        if ( -1 != program_str.find(PROGRAM_TECH_HIGH_SCHOOL_PRIV) ):
            return (True)
        return (False)

    def __get_program_scholarship_status_from_string(self, program_str):
        if ( -1 != program_str.find(PROGRAM_NO_SCHOLARSHIP_STRING) ):
            return (0)
        elif ( -1 != program_str.find(PROGRAM_SCHOLARSHIP_MARKER_STRING) ):
            if ( -1 != program_str.find(PROGRAM_FULL_SCHOLARSHIP_STRING) ):
                return (100)
            elif ( -1 != program_str.find(PROGRAM_25_PER_SCHOLARSHIP_STRING) ):
                return (25)
            elif ( -1 != program_str.find(PROGRAM_50_PER_SCHOLARSHIP_STRING) ):
                return (50)
            elif ( -1 != program_str.find(PROGRAM_75_PER_SCHOLARSHIP_STRING) ):
                return (75)
            else:
                return (-2) # indicates error
        else:
            return (-1) # indicates state university

    def __get_program_student_and_score_attributes(self, program_str):
        field_marker_idx = program_str.find(PROGRAM_FIELD_MARKER_STRING)
        if ( -1 == field_marker_idx ):
            raise MalformedProgramStateStringException(program_str)
        stats = (program_str[field_marker_idx + len(PROGRAM_FIELD_MARKER_STRING):]).split(" ")
        while '' in stats:
            stats.remove('')
        for i in range(len(stats)):
            stats[i] = stats[i].strip("\n")
        if ( len(stats) != 4 ):
            raise MalformedProgramStateStringException(program_str)
        for i in range(len(stats)):
            stats[i] = stats[i].replace(",", ".")
        if ( (stats[2] == PROGRAM_SCORE_NONE_STRING) and  (stats[3] == PROGRAM_SCORE_NONE_STRING) ):
            return [int(stats[0]), int(stats[1]), float(0), float(0)]
        return [int(stats[0]), int(stats[1]), float(stats[2]), float(stats[3])]

    def __init__(self, program_str):
        self.__name = PROGRAM_NAME_STRING
        self.__scholarship = -1
        self.__is_evening_edu = False
        self.__language = Language.TURKISH
        self.__is_tech_high_school_priv = False
        self.__student_quota = 0
        self.__num_of_student_got_in = 0
        self.__score_lower_bound = 0
        self.__score_upper_bound = 0

        self.__language = self.__get_program_lang_from_string(program_str)
        self.__is_evening_edu = self.__get_program_is_evening_edu_state_from_string(program_str)
        self.__is_tech_high_school_priv = self.__get_program_is_tech_high_school_priv_state_from_string(program_str)
        self.__scholarship = self.__get_program_scholarship_status_from_string(program_str)
        student_and_score_attr = self.__get_program_student_and_score_attributes(program_str)
        self.__student_quota = student_and_score_attr[0]
        self.__num_of_student_got_in = student_and_score_attr[1]
        self.__score_lower_bound = student_and_score_attr[2]
        self.__score_upper_bound = student_and_score_attr[3]

    def get_program_lower_bound_score(self):
        return (self.__score_lower_bound)

    def get_program_upper_bound_score(self):
        return (self.__score_upper_bound)

    def get_program_name(self):
        return (self.__name)

    def get_program_scholarship(self):
        return (self.__scholarship)

    def get_program_is_private(self):
        if ( -1 == self.__scholarship ):
            return (False)
        return (True)

    def get_program_is_evening_edu(self):
        return (self.__is_evening_edu)

    def get_program_language(self):
        return (self.__language)

    def get_program_is_tech_high_school_priv(self):
        return (self.__is_tech_high_school_priv)

    def get_program_student_quota(self):
        return (self.__student_quota)

    def get_program_num_of_student_got_in(self):
        return (self.__num_of_student_got_in)

class Faculty:
    __name = None
    __programs = None

    def __init__(self, faculty_str):
        self.check_faculty_str_fmr(faculty_str)

        self.__name = ""
        self.__programs = []

        splitted_faculty_str = faculty_str.split('/', 1)
        self.__name = splitted_faculty_str[0]
        self.add_program(faculty_str)

    def check_name(self, faculty_str):
        self.check_faculty_str_fmr(faculty_str)
        splitted_faculty_str = faculty_str.split('/', 1)
        if ( splitted_faculty_str[0] == self.__name ):
            return (True)
        return (False)

    def add_program(self, faculty_str):
        self.check_faculty_str_fmr(faculty_str)
        splitted_faculty_str = faculty_str.split('/', 1)
        self.__programs.append(Program(splitted_faculty_str[1]))

    def get_faculty_name(self):
        return (self.__name)

    def get_num_of_programs(self):
        return (len(self.__programs))

    def get_program_by_index(self, index):
        return (self.__programs[index])

    def get_program_names_in_faculty(self):
        prog_names = []
        for p in self.__programs:
            prog_names.append(self.__name + " - " + p.get_program_name())
        return (prog_names)

    def get_program_name_and_lb_score_in_faculty(self):
        prog_name_and_scores = []
        for p in self.__programs:
            prog_name_and_scores.append({'name' : self.__name + " - " + p.get_program_name(),
                                         'lb_score' : p.get_program_lower_bound_score()})
        return (prog_name_and_scores)

    def get_program_name_and_ub_score_in_faculty(self):
        prog_name_and_scores = []
        for p in self.__programs:
            prog_name_and_scores.append({'name' : self.__name + " - " + p.get_program_name(),
                                         'ub_score' : p.get_program_upper_bound_score()})
        return (prog_name_and_scores)

    def check_if_programs_have_scholarship(self):
        for i in range(len(self.__programs)):
            if ( -1 != self.__programs[i].get_program_scholarship() ):
                return (True)
        return (False)

    @staticmethod
    def check_faculty_str_fmr(faculty_str):
        faculty_str_split = faculty_str.split('/')
        if ( len(faculty_str_split) != 2 ):
            raise MalformedFacultyStringException(faculty_str)

class Univesity:
    __name = None
    __faculties = None

    def __get_faculty_idx_with_name(self, facutly_str):
        for i in range(len(self.__faculties)):
            if ( True == self.__faculties[i].check_name(facutly_str) ):
                return (i)
        return (-1)

    def __check_if_faculties_have_program_with_scholarship(self):
        for i in range(len(self.__faculties)):
            if ( True == self.__faculties[i].check_if_programs_have_scholarship() ):
                return (True)
        return (False)

    def __init__(self, uni_str):
        self.check_uni_str_fmt(uni_str)

        self.__name = ""
        self.__faculties = []

        splitted_uni_str = uni_str.split('/', 1)
        self.__name = splitted_uni_str[0]
        self.add_program(uni_str)

    def add_program(self, uni_str):
        self.check_uni_str_fmt(uni_str)
        splitted_uni_str = uni_str.split('/', 1)
        faculty_idx = self.__get_faculty_idx_with_name(splitted_uni_str[1])
        if ( -1 == faculty_idx ):
            self.__faculties.append(Faculty(splitted_uni_str[1]))
        else:
            self.__faculties[faculty_idx].add_program(splitted_uni_str[1])

    def get_university_name(self):
        return (self.__name)

    def get_num_of_faculties(self):
        return (len(self.__faculties))

    def get_faculty_by_index(self, index):
        return (self.__faculties[index])

    def get_program_names_in_university(self):
        prog_names = []
        for f in self.__faculties:
            faculty_prog_names = f.get_program_names_in_faculty()
            for faculty_prog_name in faculty_prog_names:
                prog_names.append(self.__name + " - " + faculty_prog_name)
        return (prog_names)

    def get_program_name_and_lb_scores_in_university(self):
        prog_name_and_scores = []
        for f in self.__faculties:
            faculty_prog_name_and_scores = f.get_program_name_and_lb_score_in_faculty()
            for faculty_prog_scores in faculty_prog_name_and_scores:
                prog_name_and_scores.append({'name' : self.__name + " - " + faculty_prog_scores['name'],
                                             'lb_score' : faculty_prog_scores['lb_score']})
        return (prog_name_and_scores)

    def get_program_name_and_ub_scores_in_university(self):
        prog_name_and_scores = []
        for f in self.__faculties:
            faculty_prog_name_and_scores = f.get_program_name_and_ub_score_in_faculty()
            for faculty_prog_scores in faculty_prog_name_and_scores:
                prog_name_and_scores.append({'name' : self.__name + " - " + faculty_prog_scores['name'],
                                             'ub_score' : faculty_prog_scores['ub_score']})
        return (prog_name_and_scores)

    @staticmethod
    def check_uni_str_fmt(uni_str):
        uni_str_split = uni_str.split('/')
        if ( len(uni_str_split) != 3 ):
            raise MalformedUniversityStringException(uni_str)

    @staticmethod
    def get_university_idx_from_uni_list(uni_list, uni_str):
        Univesity.check_uni_str_fmt(uni_str)
        splitted_uni_str = uni_str.split('/', 1)
        for i in range(len(uni_list)):
            if ( splitted_uni_str[0] == uni_list[i].get_university_name() ):
                return (i)
        return (-1)

if __name__ == "__main__":
    university_list = []
    fd = open("cse_results.txt", encoding = "utf8");
    while True:
        try:
            line = fd.readline()
            if ( "" == line ):
                break
            line.rstrip('\n').rstrip('\r')
            if ( "\n" != line ):
                uni_idx = Univesity.get_university_idx_from_uni_list(university_list, line)
                if ( -1 == uni_idx ):
                    university_list.append(Univesity(line))
                else:
                    university_list[uni_idx].add_program(line)

        except MalformedUniversityStringException as e:
            print (e.str)
            sys.exit(1)
        except MalformedFacultyStringException as e:
            print (e.str)
            sys.exit(1)
        except MalformedProgramStateStringException as e:
            print (e.str)
            sys.exit(1)

    fd.close()

    stat_list = []

    for u in range(len(university_list)):
        uni =  university_list[u]
        for f in range(uni.get_num_of_faculties()):
            faculty = uni.get_faculty_by_index(f)
            for p in range(faculty.get_num_of_programs()):
                prog = faculty.get_program_by_index(p)

                prog_full_name = ("%-105s %-15s %-4s %-10s %-12s" %
                                  ((str(uni.get_university_name()) + " - " + str(faculty.get_faculty_name())),
                                  (prog.get_program_is_private() and ("(%" + (("%3s") % str(prog.get_program_scholarship())) + " Burslu)") or ""),
                                  (prog.get_program_is_evening_edu() and "(İÖ)" or ""),
                                  (prog.get_program_is_tech_high_school_priv() and "(M.T.O.K.)" or ""),
                                  ((Language.ENGLISH == prog.get_program_language()) and "(İngilizce)" or
                                    ((Language.ENGLISH == prog.get_program_language()) and "(Almanca)" or ""))))

                stat_list.append({'name'                    : prog_full_name,
                                  'is_private'              : prog.get_program_is_private(),
                                  'lb_score'                : prog.get_program_lower_bound_score(),
                                  'ub_score'                : prog.get_program_upper_bound_score(),
                                  'scholarship'             : prog.get_program_scholarship(),
                                  'is_evening_edu'          : prog.get_program_is_evening_edu(),
                                  'language'                : prog.get_program_language(),
                                  'is_tech_high_school_priv': prog.get_program_is_tech_high_school_priv(),
                                  'student_quota'           : prog.get_program_student_quota(),
                                  'num_of_student_got_in'   : prog.get_program_num_of_student_got_in()})

    ###########################################################################
    stat_list.sort(key = lambda dict: dict['ub_score'], reverse = True)

    fd = open("Üniversitelerin Başarı Sırası (Tavan Puanına Göre).txt", "w")
    fd.write("...::: Üniversitelerin Başarı Sırası (Tavan Puanına Göre) :::...\n")
    for i in range(len(stat_list)):
        fd.write("%-4d - %-150s : %f\n" % (i + 1, stat_list[i]['name'], stat_list[i]['ub_score']))
    fd.write("\n")
    fd.close()

    fd = open("Devlet Üniversiteleri Başarı Sırası (Tavan Puanına Göre).txt", "w")
    fd.write("...::: Devlet Üniversiteleri Başarı Sırası (Tavan Puanına Göre) :::...\n")
    idx = 0
    for i in range(len(stat_list)):
        if ( False == stat_list[i]['is_private'] ):
            fd.write("%-4d - %-150s : %f\n" % (idx + 1, stat_list[i]['name'], stat_list[i]['ub_score']))
            idx += 1
    fd.write("\n")
    fd.close()

    fd = open("Özel Üniversiteler Başarı Sırası (Tavan Puanına Göre).txt", "w")
    fd.write("...::: Özel Üniversiteler Başarı Sırası (Tavan Puanına Göre) :::...\n")
    idx = 0
    for i in range(len(stat_list)):
        if ( True == stat_list[i]['is_private'] ):
            fd.write("%-4d - %-150s : %f\n" % (idx + 1, stat_list[i]['name'], stat_list[i]['ub_score']))
            idx += 1
    fd.write("\n")
    fd.close()

    ###########################################################################
    stat_list.sort(key = lambda dict: dict['lb_score'], reverse = True)

    fd = open("Üniversitelerin Başarı Sırası (Taban Puanına Göre).txt", "w")
    fd.write("...::: Üniversitelerin Başarı Sırası (Taban Puanına Göre) :::...\n")
    for i in range(len(stat_list)):
        fd.write("%-4d - %-150s : %f\n" % (i + 1, stat_list[i]['name'], stat_list[i]['lb_score']))
    fd.write("\n")
    fd.close()

    fd = open("Devlet Üniversiteleri Başarı Sırası (Taban Puanına Göre).txt", "w")
    fd.write("...::: Devlet Üniversiteleri Başarı Sırası (Taban Puanına Göre) :::...\n")
    idx = 0
    for i in range(len(stat_list)):
        if ( False == stat_list[i]['is_private'] ):
            fd.write("%-4d - %-150s : %f\n" % (idx + 1, stat_list[i]['name'], stat_list[i]['lb_score']))
            idx += 1
    fd.write("\n")
    fd.close()

    fd = open("Özel Üniversiteler Başarı Sırası (Taban Puanına Göre).txt", "w")
    fd.write("...::: Özel Üniversiteler Başarı Sırası (Taban Puanına Göre) :::...\n")
    idx = 0
    for i in range(len(stat_list)):
        if ( True == stat_list[i]['is_private'] ):
            fd.write("%-4d - %-150s : %f\n" % (idx + 1, stat_list[i]['name'], stat_list[i]['lb_score']))
            idx += 1
    fd.write("\n")
    fd.close()

    ###########################################################################

    fd = open("Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı.txt", "w")
    fd.write("...::: Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı :::...\n")
    total_student_quota = 0
    total_num_of_student_got_in = 0
    for i in range(len(stat_list)):
        total_student_quota += stat_list[i]['student_quota']
        total_num_of_student_got_in += stat_list[i]['num_of_student_got_in']
    fd.write("Toplam Kontenjan               : %d.\n" % (total_student_quota))
    fd.write("Toplam Yerleşen Öğrenci Sayısı : %d.\n" % (total_num_of_student_got_in))
    fd.write("Boşta Kalan Kontejan Sayısı    : %d.\n" % (total_student_quota - total_num_of_student_got_in))
    fd.write("\n")
    fd.close()

    ###########################################################################

    fd = open("Devlet Üniversiteleri Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı.txt", "w")
    fd.write("...::: Devlet Üniversiteleri Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı :::...\n")
    state_uni_total_student_quota = 0
    state_uni_total_num_of_student_got_in = 0
    for i in range(len(stat_list)):
        if ( False == stat_list[i]['is_private'] ):
            state_uni_total_student_quota += stat_list[i]['student_quota']
            state_uni_total_num_of_student_got_in += stat_list[i]['num_of_student_got_in']
    fd.write("Toplam Kontenjan               : %d.\n" % (state_uni_total_student_quota))
    fd.write("Toplam Yerleşen Öğrenci Sayısı : %d.\n" % (state_uni_total_num_of_student_got_in))
    fd.write("Boşta Kalan Kontejan Sayısı    : %d.\n" % (state_uni_total_student_quota -
                                                                 state_uni_total_num_of_student_got_in))
    fd.write("\n")
    fd.close()

    ###########################################################################

    fd = open("Özel Üniversitelerin Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı.txt", "w")
    fd.write("...::: Özel Üniversitelerin Toplam Kotenjan ve Toplam Yerleşen Öğrenci Sayısı :::...\n")
    priv_uni_total_student_quota = 0
    priv_uni_total_num_of_student_got_in = 0
    for i in range(len(stat_list)):
        if ( True == stat_list[i]['is_private'] ):
            priv_uni_total_student_quota += stat_list[i]['student_quota']
            priv_uni_total_num_of_student_got_in += stat_list[i]['num_of_student_got_in']
    fd.write("Toplam Kontenjan               : %d.\n" % (priv_uni_total_student_quota))
    fd.write("Toplam Yerleşen Öğrenci Sayısı : %d.\n" % (priv_uni_total_num_of_student_got_in))
    fd.write("Boşta Kalan Kontejan Sayısı    : %d.\n" % (priv_uni_total_student_quota -
                                                                 priv_uni_total_num_of_student_got_in))
    fd.write("\n")
    fd.close()

    sys.exit(0)
