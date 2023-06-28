from sqlalchemy import func, desc, and_, distinct, select

from src.db import session
from src.models import Teacher, Student, Discipline, Grade, Group


def select_one():  # Найти 5 студентов с наибольшим средним баллом по всем предметам.
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()

    return result


def select_two(discipline_id):  # Найти студента с наивысшим средним баллом по определенному предмету.
    result = session.query(Student.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()

    return result


def select_three(discipline_id):  # Найти средний балл в группах по определенному предмету.
    result = session.query(Discipline.name, Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.name, Discipline.name).all()

    return result


def select_four():  # Найти средний балл на потоке (по всей таблице оценок).
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .all()

    return result


def select_five(teacher_id):  # Найти какие курсы читает определенный преподаватель.
    result = session.query(Discipline.name, Teacher.fullname) \
        .select_from(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .all()

    return result


def select_six(group_id):  # Найти список студентов в определенной группе.
    result = session.query(Student.fullname, Group.name) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .all()

    return result


def select_seven(group_id, discipline_id):  # Найти оценки студентов в отдельной группе по определенному предмету.
    result = session.query(Student.fullname, Grade.grade) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(and_(Student.group_id == group_id, Grade.discipline_id == discipline_id)) \
        .order_by(Discipline.name) \
        .all()

    return result


def select_eight():  # Найти средний балл, который ставит определенный преподаватель по своим предметам.
    result = session.query(distinct(Teacher.fullname), func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter_by(id=3) \
        .group_by(Teacher.fullname) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()

    return result


def select_nine(student_id):  # Найти список курсов, которые посещает определенный студент.
    result = session.query(Student.fullname, Discipline.name) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Grade.student_id == student_id) \
        .group_by(Student.fullname, Discipline.name) \
        .all()

    return result


def select_ten(student_id, teacher_id):  # Список курсов, которые определенному студенту читает определенный
    # преподаватель.
    sub_query = (select(Discipline.id).where(Discipline.teacher_id == teacher_id).scalar_subquery())

    result = session.query(Discipline.name) \
        .select_from(Grade) \
        .join(Discipline) \
        .filter(and_(Grade.discipline_id.in_(sub_query), Grade.student_id == student_id)) \
        .group_by(Discipline.name) \
        .all()

    return result


if __name__ == '__main__':
    # print(select_one())
    # print(select_two(5))
    # print(select_three(3))
    # print(select_four())
    # print(select_five(3))
    # print(select_six(2))
    # print(select_seven(1, 5))
    # print(select_eight())
    # print(select_nine(1))
    print(select_ten(42, 4))
