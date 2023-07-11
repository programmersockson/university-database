from random import randint

from schema import *

session = Session(bind=engine)

# - - - - add 10 students - - - -
names = ["Boris Scherba", "Veronika Zayac", "Vitali Zavodski", "Nastya Bukina", "Masha Pikulina",
         "Maksim Boreckiy", "Georgi Masluk", "Anatoli Morsich", "Oleg Babushkin", "Vyacheslav Tolmachev"]

for i in range(10):
    c = randint(1, 4)
    y = 2023 - c - 1
    d_o_a = f"{y}-09-01"
    stud = Student(
        full_name=names[i],
        course=c,
        group_num=randint(1, 10),
        date_of_admission=d_o_a
    )
    session.add(stud)

kkk = Student(
    full_name="Katie Carbon",
    course=2,
    group_num=5,
    date_of_admission="2022-09-01"
)
session.add(kkk)

students = session.query(Student).all()

for s in students:
    print("ID: ", s.student_id, "Name: ", s.full_name)

# - - - - - - - - - - - - - - -

# - - - - add 4 teachers - - - -
names = ["Alex Makedonski", "Elizabeth II", "Dmitri Palamarchuk", "Stella Solar"]
deg = ["Polkovodec", "Queen", "Foma", "Fairy"]

for i in range(4):
    teac = Teacher(
        full_name=names[i],
        degree=deg[i]
    )
    session.add(teac)

teachers = session.query(Teacher).all()

for t in teachers:
    print("ID: ", t.teacher_id, "Name: ", t.full_name, "Degree: ", t.degree)

# - - - - - - - - - - - - - - -

# - - - - add 4 subjects - - - -
names = ["Algebra", "Geometry", "PE", "LSF"]

for i in range(4):
    sub = Subject(
        name=names[i],
        has_test=randint(0, 1),
        has_exam=randint(0, 1)
    )
    session.add(sub)

subjects = session.query(Subject).all()

for s in subjects:
    print("ID: ", s.subject_id, "Name: ", s.name)

# - - - - - - - - - - - - - - -

session.commit()
