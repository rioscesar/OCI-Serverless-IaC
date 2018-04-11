import fdk
import json


def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {'name': 'World'}

    # todo: need to pass in the vcn to this thing as well as an image_id.
    # todo: we are also creating private keys for the user using the metadata option
    # pass in or create one for them
    
    print('Creating compute instance ...')
    compute_details = LaunchInstanceDetails(
        availability_domain = self.subnet.availability_domain,
        compartment_id = self.config['compartment'],
        display_name = self.name,
        # todo: remove reference to operating_system
        image_id = self.operating_systems[self.config['image_os']],
        shape = self.config['shape'],
        subnet_id = self.subnet.id,
        metadata = self.create_metadata()
    )
    while True:
        try:
            self.compute_instance = self.client.launch_instance(compute_details).data
            return get_vnic(vcn)
        except Exception as e:
            continue

# todo: make this play nice with compute creation  
def get_vnic(self, vcn):
    while True:
        vnic_attachments = self.client.list_vnic_attachments(self.config['compartment']).data
        for attachment in vnic_attachments:
            if self.compute_instance.id == attachment.instance_id:
                vnic = vcn.client.get_vnic(attachment.vnic_id).data
                self.public_ip = vnic.public_ip
                self.private_ip = vnic.private_ip
                return

# todo: remove mention of writing to file : write straight to the database            
def create_metadata(self):
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    self.private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        crypto_serialization.NoEncryption())
    self.public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    with open('./'+self.keyfile, 'w+') as f:
        # todo: this gets returned for the user to download
        os.chmod('./'+self.keyfile, 0o600)
        f.write(self.private_key.decode())
        print('Created private ssh key - "./'+self.keyfile+'"')
        metadata = {
            'ssh_authorized_keys': self.public_key.decode()
        }
    return metadata



if __name__ == '__main__':
    fdk.handle(handler)
