import fdk
import json
import oci

from flask_app.app.schemas.vcn import VCNSchema


def handler(ctx, data=None, loop=None):
    body = json.loads(data)
    cidr_block = body['cidr_block']
    name = body.get('name', 'vcn_name')
    compartment_id = body['compartment_id']

    config = body['environment']

    virtual_network = oci.core.VirtualNetworkClient(config)
    
    vcn_name = name
    result = virtual_network.create_vcn(
        oci.core.models.CreateVcnDetails(
            cidr_block=cidr_block,
            display_name=vcn_name,
            compartment_id=compartment_id
        )
    )
    get_vcn_response = oci.wait_until(
        virtual_network,
        virtual_network.get_vcn(result.data.id),
        'lifecycle_state',
        'AVAILABLE'
    )

    # todo: add logging to another ip
    print('Created VCN: {}'.format(get_vcn_response.data.id))
    return VCNSchema().dump(get_vcn_response.data)


if __name__ == '__main__':
    fdk.handle(handler)
