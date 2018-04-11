import fdk
import json
import oci


def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {} 
    user = body['user']
    name = body.get('name', 'gateway_name')

    # probably have to use marshmallow to serialize classes and deserialize 
    vcn = body['vcn']
    
    # use the user to find configuration on the database to be abe to connect to OCI
    # config = {db stuff with keys and values}
    virtual_network_client = oci.core.VirtualNetworkClient(config)
    
    internet_gateway_name = name
    result = virtual_network.create_internet_gateway(
        oci.core.models.CreateInternetGatewayDetails(
            display_name=internet_gateway_name,
            compartment_id=vcn.compartment_id,
            is_enabled=True,
            vcn_id=vcn.id
        )
    )
    get_internet_gateway_response = oci.wait_until(
        virtual_network,
        virtual_network.get_internet_gateway(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    print('Created internet gateway: {}'.format(get_internet_gateway_response.data.id))

    add_route_rule_to_default_route_table_for_internet_gateway(
        virtual_network,
        vcn,
        get_internet_gateway_response.data
    )

    # probably have to use marshmallow to serialize classes and deserialize 
    return get_internet_gateway_response.data

# This makes sure that we use the internet gateway for accessing the internet. See:
# https://docs.us-phoenix-1.oraclecloud.com/Content/Network/Tasks/managingIGs.htm
# for more information.
#
# As a convenience, we'll add a route rule to the default route table. However, in your
# own code you may opt to use a different route table
def add_route_rule_to_default_route_table_for_internet_gateway(virtual_network, vcn, internet_gateway):
    get_route_table_response = virtual_network.get_route_table(vcn.default_route_table_id)
    route_rules = get_route_table_response.data.route_rules

    print('\nCurrent Route Rules For VCN')
    print('===========================')
    print('{}\n\n'.format(route_rules))

    # Updating route rules will totally replace any current route rules with what we send through.
    # If we wish to preserve any existing route rules, we need to read them out first and then send
    # them back to the service as part of any update
    route_rules.append(
        oci.core.models.RouteRule(
            cidr_block='0.0.0.0/0',
            network_entity_id=internet_gateway.id
        )
    )

    virtual_network.update_route_table(
        vcn.default_route_table_id,
        oci.core.models.UpdateRouteTableDetails(route_rules=route_rules)
    )

    get_route_table_response = oci.wait_until(
        virtual_network,
        virtual_network.get_route_table(vcn.default_route_table_id),
        'lifecycle_state',
        'AVAILABLE'
    )

    print('\nUpdated Route Rules For VCN')
    print('===========================')
    print('{}\n\n'.format(get_route_table_response.data.route_rules))

    return get_route_table_response.data


if __name__ == '__main__':
    fdk.handle(handler)
