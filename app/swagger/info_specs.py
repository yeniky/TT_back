from http import HTTPStatus
from app.schemas import InfoSchema

get_spec = {
    'tags': ['Info'],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'To get App Info',
            'schema': InfoSchema
        }
    }
}

put_spec = {
    'tags': ['Info'],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Set app info',
            'schema': InfoSchema
        }
    },
    'parameters': [
        {
            'in': 'body',
            'name': 'info',
            'schema': InfoSchema,
            'required': True
        }]
}
