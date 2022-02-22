from http import HTTPStatus
from app.schemas import UserSchema, PasswordSchema

get_spec = {
    'tags': ['Users'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'User list',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': UserSchema
                    },
                    'page': {
                        'type': 'integer',
                        'description': 'Number of current page'
                    },
                    'per_page': {
                        'type': 'integer',
                        'description': 'Number of items per page'
                    },
                    'has_next': {
                        'type': 'boolean',
                        'description': 'True if there is a next page'
                    },
                    'total_pages': {
                        'type': 'integer',
                        'description': 'Total number of pages'
                    },
                    'total': {
                        'type': 'integer',
                        'description': 'Total items in current query'
                    }
                }
            }
        }
    }
}

login_spec = {
    'tags': ['Users'],
    'security': [{'BasicAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'User info',
            'schema': UserSchema
        }
    }
}

post_spec = {
    'tags': ['Users'],
    'security': [{'BearerAuth': []}],
    'description': 'Add user by email',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'User created',
            'schema': UserSchema
        }
    },
    'parameters': [{
        'in': 'body',
        'name': 'user',
        'schema': UserSchema,
        'required': True
    }]
}

put_spec = {
    'tags': ['Users'],
    'description': 'Edit username email',
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Edited user',
            'schema': UserSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'User id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    },
        {
        'in': 'body',
        'name': 'user',
        'schema': UserSchema,
        'required': True
    }]
}

token_spec = {
    'tags': ['Users'],
    'security': [{'BasicAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'User token',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {
                        'type': 'string'
                    },
                    'example':   {
                        "token": "UmZ3SU+2jap4laAcv6BlKjHOUw0jnceD"
                    }
                }
            }
        }
    }
}

pass_spec = {
    'tags': ['Users'],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': "OK"
        }
    },
    'parameters': [{
        'in': 'body',
        'name': 'password change params',
        'schema': PasswordSchema,
        'required': True
    }]
}

delete_spec = {
    'tags': ['Users'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'User id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    }]
}

act_spec = {
    'tags': ['Users'],
    'responses': {
        HTTPStatus.OK.value: {
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Activation Token',
        'name': 'token',
        'schema': {
            'type': 'string'},
        'required': True
    }, {
        'in': 'body',
        'description': 'Username',
        'name': 'username',
        'schema': {
            'type': 'string'},
        'required': True
    },
        {
        'in': 'body',
        'description': 'Password',
        'name': 'password',
        'schema': {
            'type': 'string'},
        'required': True
    }]
}
