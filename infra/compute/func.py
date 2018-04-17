import fdk
import json
import oci
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def handler(ctx, data=None, loop=None):
    body = json.loads(data)

    ad = body['ad']
    compartment_id = body['compartment_id']
    name = body.get('name', 'instance')
    image_id = body['image_id']
    # todo: find a way to get the shape to the frontend
    # list_shapes(compartment_id)
    shape = body['shape']
    subnet_id = body['subnet_id']

    config = body['environment']

    metadata, private_key = create_metadata()

    compute_details = oci.core.models.LaunchInstanceDetails(
        availability_domain=ad,
        compartment_id=compartment_id,
        display_name=name,
        source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=image_id),
        shape=shape,
        metadata=metadata,
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id=subnet_id
        )
    )

    compute_client = oci.core.compute_client.ComputeClient(config)
    vcn = oci.core.VirtualNetworkClient(config)

    compute_instance = compute_client.launch_instance(compute_details).data

    oci.wait_until(
        compute_client,
        compute_client.get_instance(compute_instance.data.id),
        'lifecycle_state',
        'RUNNING'
    )
    return compute_instance
    # return get_vnic(vcn, compute_client, compartment_id, compute_instance.id), private_key


def get_vnic(vcn, client, compartment_id, compute_id):
    while True:
        vnic_attachments = client.list_vnic_attachments(compartment_id).data
        for attachment in vnic_attachments:
            if compute_id == attachment.instance_id:
                vnic = vcn.get_vnic(attachment.vnic_id).data

                return vnic.public_ip, vnic.public_ip


def create_metadata():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    metadata = {
        'ssh_authorized_keys': public_key.decode()
    }
    return metadata, private_key.decode()


if __name__ == '__main__':
    fdk.handle(handler)
