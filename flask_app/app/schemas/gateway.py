from marshmallow import fields, Schema


class GatewaySchema(Schema):
    """
    Marshmallow Schema class for the Gateway Object.
    """

    id = fields.String()
    compartment_id = fields.String()
    display_name = fields.String()
    is_enabled = fields.String()
    lifecycle_state = fields.String()
    time_created = fields.String()
    vcn_id = fields.String()
