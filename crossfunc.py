import pandas as pd


def check_code_subj(data):
    '''Compares course code with concatenated course subject and course number'''
    course_code = data["Course Code (CB01)"]
    course_subj = data["Course Subject* (CB01)"]
    course_number = data["Course Number* (CB01)"]
    course_code2 = course_subj.astype(str) + course_number.astype(str)

    return list(course_code[course_code != course_code2].index)


def check_subj_num_id(data):
    '''Compares curriculum id with concatenated course subject and course number'''
    curriculum_id = data["Curriculum Id*"]
    course_subj = data["Course Subject* (CB01)"]
    course_number = data["Course Number* (CB01)"]
    course_code2 = "C" + course_subj.astype(str) + "-" + course_number.astype(str)

    return list(curriculum_id[curriculum_id != course_code2].index)


def check_code_id(data):
    '''Compares a stripped curriculum id with course code'''
    curriculum_id = data["Curriculum Id*"]
    course_code = data["Course Code (CB01)"]
    curriculum_id2 = curriculum_id.str[1:]
    out = curriculum_id2.str.replace('-', '')

    return list(course_code[out != course_code].index)


def check_cross_walk(data):
    '''Compares curriculum id with crosswalk name and number'''
    check = data["Course Crosswalk Crs Dept Name (CB19)"].astype(str) + "-" + data["Course Crosswalk Crs Number (CB20)"].astype(str)
    curriculum_id = data["Curriculum Id*"]

    return list(curriculum_id[curriculum_id != check].index)


# Capture functions as a list for easy import
check_functions = [check_code_subj, check_subj_num_id, check_code_id, check_cross_walk]

if __name__ == '__main__':

    data = pd.read_excel('import.xlsx', engine='openpyxl')

    print(check_code_subj(data))

    print(check_subj_num_id(data))

    print(check_code_id(data))

    print(check_cross_walk(data))
