from sqlalchemy import func, desc, and_, distinct, select

from src.db import session
from src.models import Teacher, Student, Discipline, Grade, Group


def select_one():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()

    return result


def select_two():
    result = session.query(Student.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()

    return result


def select_three():
    result = session.query(Student.group_id, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.teacher_id == Discipline.id) \
        .group_by(Discipline.id).all()

    return result


def select_eight():
    result = session.query(distinct(Teacher.fullname), func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter_by(id=3) \
        .group_by(Teacher.fullname) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()

    return result


if __name__ == '__main__':
    # print(select_one())
    # print(select_two())
    print(select_three())
    # print(select_eight())
