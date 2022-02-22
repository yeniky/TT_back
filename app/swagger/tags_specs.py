from http import HTTPStatus
from app.schemas import TagSchema, TagConfigSchema, ZoneEntrySchema, PositionSchema

get_spec = {
    'tags': ['Tags'],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Tag list',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': TagSchema
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

post_spec = {
    'tags': ['Tags'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Set tag configuration',
            'schema': TagSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Tag id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    },
        {
        'in': 'body',
        'description': 'Notes: \n Type must be a string with value in [Object,Person,Vehicle]. \n alert_type posible values are: [Entry, Exit, Permanence]. \n Time only requiered when alert_type=Permanence \n Zone name nor required, only id',
        'name': 'config',
        'schema': TagConfigSchema,
        'required': True
    }]
}

get_history_spec = {
    'tags': ['Tags'],
    'description': 'To get zone history of the tag',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Zone history of the tag',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': ZoneEntrySchema
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
    },
    'parameters': [{
        'in': 'path',
        'description': 'Tag id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    }]
}

get_position_spec = {
    'tags': ['Tags'],
    'description': 'To get position history of the tag',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Position history of the tag',
            'schema': PositionSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Tag id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    },
        {
        'in': 'query',
        'description': 'Start date of the position. Format: %Y-%m-%d',
        'name': 'start_date',
        'schema': {
            'type': 'string'},
        'required': True
    },
        {
        'in': 'query',
        'description': 'End date of the position. Format: %Y-%m-%d',
        'name': 'end_date',
        'schema': {
            'type': 'string'},
        'required': True
    },
        {
        'in': 'query',
        'description': 'Max count of positions',
        'name': 'count',
        'schema': {
            'type': 'integer'},
        'required': False
    }, ]
}

post_active_spec = {
    'tags': ['Tags'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Set tag active value',
            'schema': TagSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Tag id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    },
        {
        'in': 'query',
        'description': 'Active value(Tag)',
        'name': 'active',
        'schema': {
            'type': 'boolean'},
        'required': True
    }]
}
