from marshmallow import fields, Schema


class EnvironmentSchema(Schema):
    """
    Marshmallow Schema class for the Environment model.
    """

    id = fields.Integer()

    private_key = fields.String()
    user_ocid = fields.String()
    fingerprint = fields.String()
    tenancy_ocid = fields.String()

