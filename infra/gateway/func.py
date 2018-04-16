import fdk
import json
import oci


def handler(ctx, data=None, loop=None):
    body = json.loads(data)

    name = body.get('name', 'gateway_name')
    compartment_id = body['compartment_id']
    vcn_id = body['vcn_id']
    default_route_table_id = body['default_route_table_id']
    config = body['environment']

    virtual_network = oci.core.VirtualNetworkClient(config)
    
    internet_gateway_name = name
    result = virtual_network.create_internet_gateway(
        oci.core.models.CreateInternetGatewayDetails(
            display_name=internet_gateway_name,
            compartment_id=compartment_id,
            is_enabled=True,
            vcn_id=vcn_id
        )
    )
    get_internet_gateway_response = oci.wait_until(
        virtual_network,
        virtual_network.get_internet_gateway(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    # print('Created internet gateway: {}'.format(get_internet_gateway_response.data.id))

    add_route_rule_to_default_route_table_for_internet_gateway(
        virtual_network,
        default_route_table_id,
        get_internet_gateway_response.data
    )

    # probably have to use marshmallow to serialize classes and deserialize 
    return result.data


# This makes sure that we use the internet gateway for accessing the internet. See:
# https://docs.us-phoenix-1.oraclecloud.com/Content/Network/Tasks/managingIGs.htm
# for more information.
#
# As a convenience, we'll add a route rule to the default route table. However, in your
# own code you may opt to use a different route table
def add_route_rule_to_default_route_table_for_internet_gateway(virtual_network, default_route_table_id, internet_gateway):
    get_route_table_response = virtual_network.get_route_table(default_route_table_id)
    route_rules = get_route_table_response.data.route_rules

    # print('\nCurrent Route Rules For VCN')
    # print('===========================')
    # print('{}\n\n'.format(route_rules))

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
        default_route_table_id,
        oci.core.models.UpdateRouteTableDetails(route_rules=route_rules)
    )

    get_route_table_response = oci.wait_until(
        virtual_network,
        virtual_network.get_route_table(default_route_table_id),
        'lifecycle_state',
        'AVAILABLE'
    )

    # print('\nUpdated Route Rules For VCN')
    # print('===========================')
    # print('{}\n\n'.format(get_route_table_response.data.route_rules))

    return get_route_table_response.data


if __name__ == '__main__':
    fdk.handle(handler)
