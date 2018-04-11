import fdk
import json
import oci


def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {} 
    user = body['user']
    name = body.get('name', 'subnet_name')
    availability_domain = body['ad']

    # probably have to use marshmallow to serialize classes and deserialize 
    vcn = body['vcn']
    
    # use the user to find configuration on the database to be abe to connect to OCI
    # config = {db stuff with keys and values}
    virtual_network = oci.core.VirtualNetworkClient(config)
    
    subnet_name = name
    result = virtual_network.create_subnet(
        oci.core.models.CreateSubnetDetails(
            compartment_id=vcn.compartment_id,
            availability_domain=availability_domain,
            display_name=subnet_name,
            vcn_id=vcn.id,
            cidr_block=vcn.cidr_block
        )
    )
    get_subnet_response = oci.wait_until(
        virtual_network,
        virtual_network.get_subnet(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    print('Created Subnet: {}'.format(get_subnet_response.data.id))
    # probably have to use marshmallow to serialize classes and deserialize 
    return get_subnet_response.data


if __name__ == '__main__':
    fdk.handle(handler)
