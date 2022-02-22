from http import HTTPStatus
from app.schemas import ZoneSchema, ZoneEntrySchema

get_spec = {
    'tags': ['Zones'],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Zone list',
            'schema': ZoneSchema
        }
    }
}

post_spec = {
    'tags': ['Zones'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Create zone',
            'schema': ZoneSchema
        }
    },
    'parameters': [{
        'in': 'body',
        'description': 'Notes: \n tag_type must be a string with value in [Object,Person,Vehicle]\n Alert_type posible values are: [Entry, Exit, Permanence].\n Time only requiered when alert_type=Permanence',
        'name': 'zone',
        'schema': ZoneSchema,
        'required': True
    }]
}

put_spec = {
    'tags': ['Zones'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Edit zone',
            'schema': ZoneSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Zone id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    },
        {
        'in': 'body',
        'description': 'Notes: \n tag_type must be a string with value in [Object,Person,Vehicle]\n Alert_type posible values are: [Entry, Exit, Permanence].\n Time only requiered when alert_type=Permanence',
        'name': 'zone',
        'schema': ZoneSchema,
        'required': True
    }]
}


get_history_spec = {
    'tags': ['Zones'],
    'description': 'To get tag entry history of the zone',
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
        'description': 'Zone id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    }]
}

post_deactive_spec = {
    'tags': ['Zones'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Deactive zone',
            'schema': ZoneSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Zone id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    }]
}
