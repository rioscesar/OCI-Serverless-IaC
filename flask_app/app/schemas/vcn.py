from marshmallow import fields, Schema


class VCNSchema(Schema):
    """
    Marshmallow Schema class for the VCN Object.
    """

    id = fields.String()

    cidr_block = fields.String()
    compartment_id = fields.String()
    default_dhcp_options_id = fields.String()
    default_route_table_id = fields.String()
    default_security_list_id = fields.String()
    display_name = fields.String()
    dns_label = fields.String()
    lifecycle_state = fields.String()
    time_created = fields.Integer()
    vcn_domain_name = fields.String()
