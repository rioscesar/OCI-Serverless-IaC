from flask import Flask, request
import requests

app = Flask(__name__)
headers = {'content-type': 'application/json'}
url = 'localhost:8080/r'

@app.route('/')
def hello():
    return 'Hello World!'

# todo: add quotes to everything

@app.route('/setup')
def setup():
    data = {
        user_id: request.args.get('user_id'),
        fingerprint: request.args.get('fingerprint'),
        private_key: request.args.get('private_key'),
        user_ocid: request.args.get('user_ocid'),
        tenancy_ocid: request.args.get('tenancy_ocid')
    }

    # todo : pass this into the database to associate the user to an environment

@app.route('/vcn')
def vcn():
    data = {
        compartment_id: request.args.get('compartment_id'),
        cidr_block: request.args.get('cidr_block'),
        name: request.args.get('name'),
        user_id: request.args.get('user_id')
    }

    # todo : pass this into the fn server
    # hardcoding the endpoint is not nice
    requests.post(url+'/infra/vcn', data=json.dumps(data), headers=headers)

@app.route('/subnet')
def subnet():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        user_id: request.args.get('user_id'),
        vcn: request.args.get('vcn_data_might_be_more_things'),
        ad: request.args.get('availability_domain'),
    }

    # todo : pass this into the fn server
    # hardcoding the endpoint is not nice
    requests.post(url+'/infra/subnet', data=json.dumps(data), headers=headers)

@app.route('/gateway')
def gateway():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        user_id: request.args.get('user_id'),
        vcn: request.args.get('vcn_data_might_be_more_things')
    }

    # todo : pass this into the fn server
    # hardcoding the endpoint is not nice
    requests.post(url+'/infra/gateway', data=json.dumps(data), headers=headers)

@app.route('/images')
def images():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        user_id: request.args.get('user_id'),
        os: request.args.get('operating_system'),
        os_version: request.args.get('operating_system_version'),
        shape: request.args.get('shape')
    }

    # todo : pass this into the fn server
    # hardcoding the endpoint is not nice
    requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)

@app.route('/compute')
def compute():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        user_id: request.args.get('user_id'),
        ad: request.args.get('operating_system'),
        compartment_id: request.args.get('operating_system_version'),
        name: request.args.get('shape'),
        image_id: request.args.get('shape'),
        shape: request.args.get('shape'),
        # could get id and ad from subnet info
        subnet_id: request.args.get('shape'),
        # todo: this is the vcn object. Find out what values are needed
        vcn: request.args.get('shape')
    }

    # todo : pass this into the fn server
    # hardcoding the endpoint is not nice
    requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
