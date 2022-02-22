from app.models import Info


def app_info():
    return Info.query.get(1)
