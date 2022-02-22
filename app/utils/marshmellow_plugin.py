def enum_to_properties(self, field, **kwargs):
    """
    Add an OpenAPI extension for marshmallow_enum.EnumField instances
    """
    import marshmallow_enum
    if isinstance(field, marshmallow_enum.EnumField):
        return {'type': 'string', 'enum': [m.name for m in field.enum]}
    return {}
