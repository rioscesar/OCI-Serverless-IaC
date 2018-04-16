from marshmallow import fields, Schema


class SubnetSchema(Schema):
    """
    Marshmallow Schema class for the Subnet Object.
    """

    id = fields.String()

    availability_domain = fields.String()
    cidr_block = fields.String()
    compartment_id = fields.String()
    default_dhcp_options_id = fields.String()

    route_table_id = fields.String()
    security_list_ids = fields.String()

    display_name = fields.String()
    dns_label = fields.String()
    lifecycle_state = fields.String()
    time_created = fields.Integer()
    vcn_domain_name = fields.String()
    prohibit_public_ip_on_vnic = fields.Boolean()
    subnet_domain_name = fields.String()
    vcn_id = fields.String()
    virtual_router_ip = fields.String()
    virtual_router_mac = fields.String()
