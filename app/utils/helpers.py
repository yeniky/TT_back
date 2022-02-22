import math
from math import sqrt
import secrets
import string
from itsdangerous import URLSafeTimedSerializer
from config import Config

alphabet = string.ascii_letters + string.digits
config = Config()


def generate_order_by(query, table, order_by, order, with_join=True):
    join_tables, order_column = get_column(table, order_by)
    if(join_tables is not None and with_join):
        query = query.join(*join_tables, isouter=True)
    if(order_column is not None):
        order_column = order_column.nullslast(
        ) if order == "asc" else order_column.desc().nullslast()
        query = query.order_by(order_column)
    return query


def get_column(table, order_by):
    elems = order_by.split('.')
    if len(elems) == 1 and elems[0] in table.__table__.columns.keys():
        return (None, table.__table__.columns[elems[0]])

    # if len(elems) == 2 and elems[0] in table.__mapper__.relationships.keys():
    #     join_table = table.__mapper__.relationships[elems[0]].mapper.class_
    #     join_table_columns = join_table.__table__.columns
    #     if elems[1] in join_table_columns.keys():
    #         return (join_table, join_table_columns[elems[1]])

    current_table = table
    join_tables = []
    if len(elems) > 1:
        for i in range(len(elems)-1):
            if(elems[i] in current_table.__mapper__.relationships.keys()):

                join_table = current_table.__mapper__.relationships[elems[i]].mapper.class_
                current_table = join_table
                join_tables.append(current_table)

                if(i+1 == len(elems)-1):
                    join_table_columns = join_table.__table__.columns
                    if elems[i+1] in join_table_columns.keys():
                        return (join_tables, join_table_columns[elems[i+1]])

    return (None, None)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    return serializer.dumps(email, salt=config.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600000):
    serializer = URLSafeTimedSerializer(config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=config.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email


def generate_password(len=20):
    password = ''.join(secrets.choice(alphabet) for i in range(len))
    return password


def build_page(schema, page, order_by, order, mapper=None):
    items = page.items
    if(mapper):
        items = [mapper(x) for x in page.items]
    return {'items': schema.dump(items), 'page': page.page, 'per_page': page.per_page, 'has_next': page.has_next, 'total_pages': page.pages, 'total': page.total, 'order_by': order_by, 'order': order}


def transformation_cords(x, y):
    # x_offset = 266
    # y_offset = 557
    # scale = 0.09618
    # return (x*scale+x_offset, y*scale+y_offset)
    return (x, y)


def ray_tracing_method(x, y, zone):
    return (zone.min_x < x <= zone.max_x) and (zone.min_y < y <= zone.max_y)


class Utils:
    @ staticmethod
    def parse_message(message: str):
        parsed_message = message.split(",")
        if len(parsed_message) != 8:
            return "invalid message"
        x = float(parsed_message[3])
        y = float(parsed_message[4])
        z = float(parsed_message[5])
        if math.isnan(x) or math.isnan(y) or math.isnan(z):
            return "invalid message"
        parsed_cords = transformation_cords(x, y)
        return {
            "addr": parsed_message[2],
            "x": parsed_cords[0],
            "y": parsed_cords[1],
            "z": z,
            "signal": float(parsed_message[6])
        }

    @ staticmethod
    def check_zones(point, zones):
        for zone in zones:
            in_zone = ray_tracing_method(point[0], point[1], zone)
            if in_zone:
                return zone
        return None

    @ staticmethod
    def get_distance(p1_x, p1_y, p2_x, p2_y):
        return sqrt((p1_x - p2_x)**2 + (p1_y - p2_y)**2)
