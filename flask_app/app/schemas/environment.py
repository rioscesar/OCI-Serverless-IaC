from marshmallow import fields, Schema


class EnvironmentSchema(Schema):
    """
    Marshmallow Schema class for the Environment model.
    """

    id = fields.Integer()

    key_content = fields.String(attribute='private_key')
    user = fields.String(attribute='user_ocid')
    fingerprint = fields.String()
    tenancy = fields.String(attribute='tenancy_ocid')
    region = fields.String()

