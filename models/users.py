import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String, nullable=True)
    number = sa.Column(sa.String, nullable=True)
    money = sa.Column(sa.String, nullable=True)
    spins = sa.Column(sa.String, nullable=True)
    mission = sa.Column(sa.String, nullable=True)
