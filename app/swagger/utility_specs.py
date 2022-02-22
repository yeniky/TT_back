from http import HTTPStatus

post_spec = {
    'tags': ['Utility'],
    'description': 'Convert table to pdf/xls format',
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'File',
            'schema': {
                'type': 'file'
            }

        }
    },
    'parameters': [{
        'in': 'query',
        'description': 'Format to convert',
        'name': 'format',
        'schema': {
            'type': 'string',
            'enum': ['pdf', 'xls']},
        'required': True
    },
        {
        'in': 'body',
        'description': 'Data to convert',
        'name': 'data',
        'schema': {
            'type': 'object',
              'properties': {
                'title': {
                    'type': 'string'
                },
                  'table': {
                    'description': 'Represents the table as an array of array. First array represent columns name of the table. THe rest represent each row of the table',
                    'type': 'array'}
              },
            'example':   {
                  'title': "Exported_data",
                'table': [['a', 'b'], [1, 2], [3, 4]]
              }
        },
        'required': True
    }
    ]
}
