import fdk
import json
import oci

# todo: only work with dicts : serialize objects to dicts

def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {} 
    user = body['user']
    cidr_block = body['cidr_block']
    name = body.get('name', 'vcn_name')
    
    # use the user to find configuration on the database to be abe to connect to OCI
    # config = {db stuff with keys and values}
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

    print('Created VCN: {}'.format(get_vcn_response.data.id))
    # probably have to use marshmallow to serialize classes and deserialize
    return get_vcn_response.data


if __name__ == '__main__':
    fdk.handle(handler)
