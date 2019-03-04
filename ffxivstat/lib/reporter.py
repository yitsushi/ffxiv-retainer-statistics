from datetime import datetime, timedelta
from pony import orm
from .database import SalesHistory


def section(*, character, title, function, **args):
    print('')
    print(f'# {title}')
    print('')

    for line in function(character, **args):
      yield line

    print('')


@orm.db_session
def daily_income(character, days=7):
    query = orm.select(
        (s.date.date(), sum(s.price)) for s in SalesHistory if s.character == character
        ).order_by(orm.desc(1)).limit(days)
    yield from query


@orm.db_session
def retainer_leaderboard(character, days=3):
    query = orm.select(
        (s.retainer, sum(s.price)) for s in SalesHistory
        if s.character == character
        and s.date >= datetime.now() - timedelta(days=days)
    ).order_by(orm.desc(2))
    yield from query


@orm.db_session
def top_products(character, days=5, limit=5):
    query = orm.select(
        (s.name, orm.avg(s.price/s.quantity), s.is_hq) for s in SalesHistory
        if s.character == character
        and s.date >= datetime.now() - timedelta(days=days)
    ).order_by(orm.desc(2)).limit(limit)
    yield from query

@orm.db_session
def top_bulk_products(character, days=5, limit=5):
    query = orm.select(
        (s.name, orm.avg(s.price/s.quantity), s.is_hq, s.quantity) for s in SalesHistory
        if s.character == character
        and s.date >= datetime.now() - timedelta(days=days)
        and s.quantity > 1
    ).order_by(orm.desc(2)).limit(limit)
    yield from query

@orm.db_session
def last(character, limit=10):
    query = orm.select(
        (s.name, s.price, s.is_hq, s.quantity, s.date) for s in SalesHistory
        if s.character == character
    ).order_by(orm.desc(5)).limit(limit)
    yield from query

