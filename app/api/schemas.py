from marshmallow import Schema, fields


class UserSchema(Schema):
    """UserSchema

    Schema for serialize a User object
    """

    id = fields.Int(dump_only=True)
    email = fields.String(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
