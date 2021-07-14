import sqlalchemy

from .db_session import SqlAlchemyBase


class Goods(SqlAlchemyBase):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    SKU = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    type_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('types.id'))
    cost = sqlalchemy.Column(sqlalchemy.REAL)
