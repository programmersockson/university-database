from sqlalchemy import Integer, Float, String, Column, \
    Date, Boolean, PrimaryKeyConstraint, ForeignKeyConstraint, \
    ForeignKey, create_engine, Engine, Null
from sqlalchemy.orm import declarative_base, relationship, Session

engine = create_engine("mysql+mysqlconnector://user:password@localhost:3306/university")

Base = declarative_base()


class Student(Base):

    __tablename__ = 'Students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    course = Column(Integer, nullable=False)
    group_num = Column(Integer, nullable=False)
    test_retakes = Column(Integer, default=0)
    access = Column(Boolean, default=True)
    exam_retakes = Column(Integer, default=0)
    expulsion = Column(Boolean, default=False)
    date_of_admission = Column(Date, nullable=False)


class Teacher(Base):

    __tablename__ = 'Teachers'

    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)


class Subject(Base):

    __tablename__ = 'Subjects'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    has_test = Column(Boolean, nullable=False)
    has_exam = Column(Boolean, nullable=False)


class Lecture(Base):

    __tablename__ = 'Lectures'

    lecture_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey('Teachers.teacher_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('Subjects.subject_id'), nullable=False)
    group_num = Column(Integer, nullable=False)
    course = Column(Integer, nullable=False)
    teacher = relationship(Teacher)
    subject = relationship(Subject)

    __table_args__ = (
        ForeignKeyConstraint(['teacher_id'], ['Teachers.teacher_id']),
        ForeignKeyConstraint(['subject_id'], ['Subjects.subject_id'])
    )


class Attendance(Base):

    __tablename__ = 'Attendance'

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'), nullable=False)
    lecture_id = Column(Integer, ForeignKey('Lectures.lecture_id'), nullable=False)
    present = Column(Boolean, nullable=False, default=True)
    student = relationship(Student)
    lecture = relationship(Lecture)

    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['Students.student_id']),
        ForeignKeyConstraint(['lecture_id'], ['Lectures.lecture_id'])
    )


class Performance(Base):

    __tablename__ = 'Performance'

    performance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'), nullable=False)
    lecture_id = Column(Integer, ForeignKey('Lectures.lecture_id'), nullable=False)
    grade = Column(Integer, nullable=True)
    student = relationship(Student)
    lecture = relationship(Lecture)

    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['Students.student_id']),
        ForeignKeyConstraint(['lecture_id'], ['Lectures.lecture_id'])
    )


class OverallPerformance(Base):

    __tablename__ = 'Overall_Performance'

    overall_performance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('Subjects.subject_id'), nullable=False)
    rating = Column(Float, nullable=True)
    exam = Column(Integer, nullable=False)
    test = Column(Boolean, nullable=False)
    student = relationship(Student)
    subject = relationship(Subject)

    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['Students.student_id']),
        ForeignKeyConstraint(['subject_id'], ['Subjects.subject_id'])
    )


Base.metadata.create_all(engine)