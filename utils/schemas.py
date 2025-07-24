from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.String(attribute="_id", dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    author = fields.String(required=True, validate=validate.Length(min=1))

class BookUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1))
    author = fields.String(validate=validate.Length(min=1))