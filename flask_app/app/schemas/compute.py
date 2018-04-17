from marshmallow import fields, Schema


class ComputeSchema(Schema):
    """
    Marshmallow Schema class for the Compute Object.
    """

    id = fields.String()
    availability_domain = fields.String()
    compartment_id = fields.String()
    display_name = fields.String()
    image_id = fields.String()
    ipxe_script = fields.String()
    launch_mode = fields.String()
    lifecycle_state = fields.String()
    # todo: need to do a dict
    # metadata
    region = fields.String()
    shape = fields.String()
    time_created = fields.Integer()
