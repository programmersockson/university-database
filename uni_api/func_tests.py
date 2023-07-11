from back_func import *

from sqlalchemy import create_engine
from random import randint

session = Session(bind=engine)

# - - - - add 10 lectures to 2 course, 5 group - - - -

subject = "Geometry"
teacher = "Elizabeth II"
course = 2
group = 5

dates = ["2023-02-02", "2023-02-17", "2023-03-01", "2023-03-14", "2023-03-30", "2023-04-10", "2023-04-22", "2023-05-01",
         "2023-05-17", "2023-06-01"]

t_id = get_teacher_id(engine, teacher)
s_id = get_subject_id(engine, subject)

for i in range(len(dates)):
    add_lecture(engine, t_id, s_id, dates[i], course, group)

# - - - - - - - - - - - - - - - - - - - - - - - -

# - - - add 1 grades to Katie Carbon student of 2 course, 5 group - - -
l_ids = [get_lecture_id(engine, i, group, course, s_id, t_id) for i in dates]
s_id = get_student_id(engine, "Katie Carbon", 2, 5)

for i in range(4):
    add_grade(engine, s_id, l_ids[i], randint(1, 10))

# - - - - - - - - - - - - - - - - - - - - - - - -
