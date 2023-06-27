"""
SOLAlchemy ORM Session
"""
from sqlalchemy import create_engine, String, ForeignKey, select, and_, or_, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column

engine = create_engine("sqlite:///:memory:", echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column()


class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User')


Base.metadata.create_all(engine)


if __name__ == '__main__':
    new_user = User(fullname="Denys Filichkin")
    session.add(new_user)
    new_address = Address(email='den@meta.ua', user=new_user)
    session.add(new_address)
    session.commit()
    new_user = User(fullname="Dima Stus")
    session.add(new_user)
    new_address = Address(email='Stus@meta.ua', user=new_user)
    session.add(new_address)
    session.commit()

    stmt = select(User.id, User.fullname)
    for row in session.execute(stmt):
        print(row.id, row.fullname)

    stmt = select(Address).join(Address.user)
    for row in session.execute(stmt):
        print(row.Address.id, row.Address.email, row.Address.user.fullname)

    stmt = select(User)
    columns = ["id", "fullname"]
    db = [dict(zip(columns, (row.User.id, row.User.fullname))) for row in session.execute(stmt)]
    print(db)

    db = [dict(zip(columns, (row.id, row.fullname))) for row in session.execute(stmt).scalars()]
    print(db)

    stmt = select(User).where(User.fullname == 'Dima Stus')
    r = session.execute(stmt).scalar_one_or_none()
    print(r.id, r.fullname)

    stmt = select(User).where(User.fullname.like("%ch%"))
    result = session.execute(stmt).scalars()
    for r in result:
        print(r.id, r.fullname)

    stmt = select(User).where(or_(User.fullname.like("%ch%"), User.id == 2))
    result = session.execute(stmt).scalars()
    for r in result:
        print(r.id, r.fullname)

    stmt = (
        select(User.fullname, func.count(Address.id))
        .join(Address)
        .group_by(User.fullname)
    )
    results = session.execute(stmt).all()
    for fullname, count in results:
        print(f"User {fullname} has {count} emails")









