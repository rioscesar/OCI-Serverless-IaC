import fdk
import json
import oci


def handler(ctx, data=None, loop=None):
    body = json.loads(data)
    compartment_id = body['compartment_id']

    config = body['environment']
    compute_client = oci.core.ComputeClient(config)

    operating_systems = {}
    images = compute_client.list_images(compartment_id).data
    for image in images:
        os = image.operating_system + " " + image.operating_system_version
        if os not in operating_systems:
            operating_systems[os] = image.id
    return operating_systems
        

if __name__ == '__main__':
    fdk.handle(handler)
