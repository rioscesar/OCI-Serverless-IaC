import fdk
import json

# create a config dict
def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {}

    # user identifier 
    app_user = body['app_user']
    
    tenancy = body['tenancy']
    user = body['user']
    fingerprint = body['fingerprint']
    private_key_content = body['private_key_content']
    pass_phrase = body.get('pass_phrase')

    # insert into the database : pass in if it was successful or not
    return True

if __name__ == '__main__':
    fdk.handle(handler)
