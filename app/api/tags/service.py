from app.models import Tag, ZoneEntry, Position, TagConfig
from app import db
import numpy as np
from sqlalchemy import text, inspect
from app.utils.helpers import generate_order_by


def tag_list(order_by, order):
    result = Tag.query
    if order_by:
        result = generate_order_by(result, Tag, order_by, order)
    return result


def set_tag_config(id, config):
    tag = Tag.query.get(id)
    if(tag):
        tag.set_config(config)
    return tag


def zone_history(id, order_by, order):
    result = ZoneEntry.query.filter_by(tag_id=id)
    if order_by:
        print(order_by)
        result = generate_order_by(result, ZoneEntry, order_by, order)
    return result


def positions_history(id, start_date, end_date, count):
    per_page = 100
    query = Position.query.filter(Position.tag_id == id).filter(
        Position.timestamp <= end_date).filter(Position.timestamp >= start_date)

    page = query.paginate(1, per_page)
    el_indexes = np.linspace(0, page.total-1, count, dtype='int')
    result = []
    if(page.total < count):
        return query.all()

    while(True):
        end = page.page*per_page if page.has_next else page.total
        indexes = list(map(lambda x: x-((page.page-1)*per_page),
                           filter(lambda x: (page.page-1)*per_page <= x < end, el_indexes)))
        result += list(np.array(page.items)[indexes])
        if(not page.has_next):
            break
        page = page.next()
    return result


def activate(id, active):
    tag = Tag.query.get(id)
    if(tag):
        tag.active = active
        db.session.commit()
    return tag
