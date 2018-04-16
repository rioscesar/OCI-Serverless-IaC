import fdk
import json
import oci


def handler(ctx, data=None, loop=None):
    body = json.loads(data)

    name = body.get('name', 'subnet_name')
    availability_domain = body['ad']
    cidr_block = body['cidr_block']
    vcn_id = body['vcn_id']
    compartment_id = body['compartment_id']

    config = body['environment']
    virtual_network = oci.core.VirtualNetworkClient(config)
    
    subnet_name = name
    result = virtual_network.create_subnet(
        oci.core.models.CreateSubnetDetails(
            compartment_id=compartment_id,
            availability_domain=availability_domain,
            display_name=subnet_name,
            vcn_id=vcn_id,
            cidr_block=cidr_block
        )
    )
    oci.wait_until(
        virtual_network,
        virtual_network.get_subnet(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )
    # print('Created Subnet: {}'.format(result.data.id))
    return result.data


if __name__ == '__main__':
    fdk.handle(handler)
