import fdk
import json

# this function is used to list all images and get their id

def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {'name': 'World'}

    # todo: remove all references to self and use body
    operating_systems = {}
    images = self.client.list_images(self.config['compartment']).data
    for image in images:
        os = image.operating_system + " " + image.operating_system_version
        if os not in operating_systems:
            operating_systems[os] = image.id
    return operating_systems
        

if __name__ == '__main__':
    fdk.handle(handler)
