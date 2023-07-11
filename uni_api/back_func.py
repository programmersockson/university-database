from schema import *

from sqlalchemy import Engine
from sqlalchemy.orm import Session


def add_lecture(engine: Engine, teacher_id: int, subject_id: int, date: str, course: int, group: int):
    session = Session(bind=engine)

    lecture_id = session.query(Lecture).count() + 1

    lecture = Lecture(
        date=date,
        teacher_id=teacher_id,
        subject_id=subject_id,
        group_num=group,
        course=course
    )
    session.add(lecture)

    students = session.query(Student).filter(Student.group_num == group,
                                             Student.course == course).all()

    student_ids = [s.student_id for s in students]
    for i in range(len(student_ids)):
        attendance = Attendance(
            student_id=student_ids[i],
            lecture_id=lecture_id
        )
        performance = Performance(
            student_id=student_ids[i],
            lecture_id=lecture_id
        )
        if not session.query(OverallPerformance).filter(OverallPerformance.subject_id == subject_id,
                                                        OverallPerformance.student_id == student_ids[i]).count():
            op = OverallPerformance(
                student_id=student_ids[i],
                subject_id=subject_id
            )
            session.add(op)
        session.add(attendance)
        session.add(performance)

    session.commit()


def get_teacher_id(engine: Engine, name: str):
    session = Session(bind=engine)
    i = session.query(Teacher).filter(Teacher.full_name == name).first()
    return i.teacher_id


def get_student_id(engine: Engine, name: str, course: int, group: int):
    session = Session(bind=engine)
    i = session.query(Student).filter(Student.full_name == name,
                                      Student.course == course,
                                      Student.group_num == group).first()
    return i.student_id


def get_subject_id(engine: Engine, name: str):
    session = Session(bind=engine)
    i = session.query(Subject).filter(Subject.name == name).first()
    return i.subject_id


def get_lecture_id(engine: Engine, date: str, group: int, course: int, subject_id: int, teacher_id: int):
    session = Session(bind=engine)
    i = session.query(Lecture).filter(Lecture.date == date,
                                      Lecture.group_num == group,
                                      Lecture.course == course,
                                      Lecture.subject_id == subject_id,
                                      Lecture.teacher_id == teacher_id).first()
    return i.lecture_id


def get_performance_id(engine: Engine, student_id: int, lecture_id: int):
    session = Session(bind=engine)
    i = session.query(Performance).filter(Performance.student_id == student_id,
                                          Performance.lecture_id == lecture_id).first()
    return i.performance_id


def get_attendance_id(engine: Engine, student_id: int, lecture_id: int):
    session = Session(bind=engine)
    i = session.query(Attendance).filter(Attendance.student_id == student_id,
                                         Attendance.lecture_id == lecture_id).first()
    return i.attendance_id


def add_grade(engine: Engine, student_id: int, lecture_id: int, grade: int):
    perf_id = get_performance_id(engine, student_id, lecture_id)
    session = Session(bind=engine)
    i = session.query(Performance).get(perf_id)
    i.grade = grade
    session.commit()


def add_absense(engine: Engine, student_id: int, lecture_id: int):
    att_id = get_attendance_id(engine, student_id, lecture_id)
    session = Session(bind=engine)
    i = session.query(Attendance).get(att_id)
    i.present = False
    session.commit()

