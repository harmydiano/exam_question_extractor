import os
import sys
from db import Db
filename = str(sys.argv[2])
exams = []
questions = []
all_questions = []
default_last_reading = 11
default_present_reading = 18
all_generated_questions = []
all_generated_answers = []
reading = {'last_reading': 0, 'present_reading': 0}

#load the db

database = Db()

def get_exam_db():
    exam_db = open_file()
    return exam_db

def open_file():
    with open(filename, "r", encoding="utf-8") as file:
        text = file.readlines()
        text = [x.strip("\n") for x in text]
        return text

def filter_punct_tags():
    exam = [x.replace("\n", "") for x in exams]
    exam = [x.replace("\ufeff", "") for x in exam]
    exam_record = dict(zip(*[iter(exam)] * 2))
    return exam_record


def extract_exam_details():
    exam_details = get_exam_db()[:6]
    exam_details = [x.split(" @") for x in exam_details]
    exam_details_length = len(exam_details)
    for count in range(exam_details_length):
        for words in exam_details[count]:
            exams.append(words.replace("@", ""))

def extract_question_details():
    exam_details = get_exam_db()[6:27]
    reading['last_reading'] = int(default_last_reading + 27)
    reading['present_reading'] = int(reading['last_reading'] + default_present_reading)

    exam_details = [x.split(" @") for x in exam_details]
    exam_details_length = len(exam_details)
    for count in range(exam_details_length):
        for words in exam_details[count]:
            questions.append(words.replace("@", ""))

def filter_punct_q_tags():
    question = [x.strip("\n") for x in questions]
    question = [x.replace("%", "").replace("<br>", "") for x in question]
    question = [x.replace("#", "") for x in question if x]
    exam_questions = dict(zip(*[iter(question[1:])] * 2))
    return question[0], exam_questions


def extract_all_question_details(start_from):
    extract_exam_details()
    extract_question_details()
    ext_exam = filter_punct_tags()
    print(filter_punct_tags())
    if start_from != '':
        start = int(start_from) + 1
    else:
        start = 1
    # print(questions)
    quest, ans = filter_punct_q_tags()
    database.insert_db(quest, "(" + ans['ANS'] + ")" + " " + ans['EXPLAN'], ans['A'],ans['B'],ans['C'],ans['D'],ext_exam['exam_id'],
                    ext_exam['class_year_id'], ext_exam['subject_id'], ans['INSTR'], ext_exam['num_views'],
                       ext_exam['examination_year'], start)
    print(quest)
    print(ans)
    while reading['present_reading'] < len(get_exam_db()):
        start = start + 1

        exam_details = get_exam_db()[reading['last_reading']:reading['present_reading']]
        reading['last_reading'] = int(default_last_reading + reading['present_reading']-2)
        reading['present_reading'] = int(reading['last_reading'] + default_present_reading)
        exam_details = [x.split(" @") for x in exam_details]
        exam_details_length = len(exam_details)
        for count in range(exam_details_length):
            for words in exam_details[count]:
                all_questions.append(words.replace("@", ""))
        filter_all_punct_q_tags(ext_exam, start)
        all_questions.clear()


def filter_all_punct_q_tags(ext_exam, start):
    print("start", start)
    question = [x.strip("\n") for x in all_questions]
    question = [x.replace("%", "").replace("<br>", "") for x in question]
    question = [x.replace("#", "") for x in question if x]
    exam_questions = dict(zip(*[iter(question[1:])] * 2))
    all_generated_questions.append(question[0])
    all_generated_answers.append(exam_questions)
    quest = question[0]
    ans = exam_questions
    print(ans)
    if 'EXPLAN' not in ans:
        ans['EXPLAN'] =  ''
    database.insert_db(quest,  "(" + ans['ANS'] + ")" + " " + ans['EXPLAN'], ans['A'], ans['B'], ans['C'], ans['D'], ext_exam['exam_id'],
                       ext_exam['class_year_id'], ext_exam['subject_id'], ans['INSTR'], ext_exam['num_views'],
                       ext_exam['examination_year'], start)
    #print (question[0])
    #print(exam_questions)
    question.clear()
    exam_questions.clear()




#all_quest, all_ans = filter_all_punct_q_tags()
#print(all_quest)
#print(all_ans)


extract_all_question_details(sys.argv[1])


