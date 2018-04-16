from marshmallow import fields, Schema


class UserSchema(Schema):
    """
    Marshmallow Schema class for the User model.
    """

    id = fields.Integer()

    user_id = fields.Integer()

    environments = fields.Nested('EnvironmentSchema', many=True, exclude=('users',))
