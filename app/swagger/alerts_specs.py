from http import HTTPStatus
from app.schemas import AlertSchema

# get_spec = {
#     'tags': ['Alerts'],
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Alerts list',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'id': {
#                         'type': 'integer'
#                     },
#                     'tag_info': {
#                         'type': 'object',
#                         'properties': {
#                             'id': {
#                                 'type': 'integer'
#                             },
#                             'address': {
#                                 'type': 'string'
#                             },
#                             'alias': {
#                                 'type': 'string',
#                                 'description': 'Only when tag is configured '
#                             }
#                         }
#                     }
#                 }


#             }
#         }
#     }
# }

get_spec = {
    'tags': ['Alerts'],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Alerts list.\n Owner type is the creator of the rule that generate the alert, Possible values: zone_alert_rule, tag_alert_rule.\n Tag_info contains id, address and alias(if apply).',
            'schema': AlertSchema
        }
    }
}
post_spec = {
    'tags': ['Alerts'],
    'security': [{'BearerAuth': []}],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Close alert',
            'schema': AlertSchema
        }
    },
    'parameters': [{
        'in': 'path',
        'description': 'Alert id',
        'name': 'id',
        'schema': {
            'type': 'integer'},
        'required': True
    }]
}

get_history_spec = {
    'tags': ['Alerts'],
    'description': 'General alert history',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'General alert history.\n Owner type is the creator of the rule that generate the alert, Possible values: zone_alert_rule, tag_alert_rule.\n Tag_info contains id, address and alias(if apply).',
            'schema': {

                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': AlertSchema
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

get_zone_history_spec = {
    'tags': ['Alerts'],
    'description': 'Alert history of zone with given id',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Note:\n Owner type is the creator of the rule that generate the alert, Possible values: zone_alert_rule, tag_alert_rule.\n Tag_info contains id, address and alias(if apply).',
            'schema': {

                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': AlertSchema
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

get_tag_history_spec = {
    'tags': ['Alerts'],
    'description': 'Alert history of tag with given id',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Note:\n Owner type is the creator of the rule that generate the alert, Possible values: zone_alert_rule, tag_alert_rule.\n Tag_info contains id, address and alias(if apply).',
            'schema': {

                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': AlertSchema
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
