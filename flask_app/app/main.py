from flask import request

import requests
import json

from flask_app.app import app, db
from flask_app.app.models import User, Environment
from flask_app.app.schemas.environment import EnvironmentSchema

headers = app.config['FN_HEADERS']
url = app.config['FN_URL']


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/setup', methods=['POST'])
def setup():

    data = request.get_json()
    
    user_id = data.get('user_id')
    fingerprint = data.get('fingerprint')
    private_key = data.get('private_key')
    user_ocid = data.get('user_ocid')
    tenancy_ocid = data.get('tenancy_ocid')
    env_name = data.get('env_name')
    region = data.get('region')

    env = Environment(env_name, private_key, user_ocid, tenancy_ocid, fingerprint, region)
    user = User(user_id, env)

    # todo: more error handling for sql inserts

    db.session.add(user)
    db.session.commit()

    return json.dumps({'success': True, 'environment': env_name}), 200, headers


@app.route('/vcn', methods=['POST'])
def vcn():
    request_data = request.get_json()

    data = {
        'compartment_id': request_data.get('compartment_id'),
        'cidr_block': request_data.get('cidr_block'),
        'name': request_data.get('name'),
        'environment': get_environment(request_data)
    }
    # todo: change name to infra
    r = requests.post(url+'/goapp/vcn', data=json.dumps(data), headers=headers)
    return r.json()


@app.route('/subnet', methods=['POST'])
def subnet():
    request_data = request.get_json()

    data = {
        'environment': get_environment(request_data),
        # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
        'vcn': request_data.get('vcn_data_might_be_more_things'),
        'ad': request_data.get('availability_domain')
    }

    requests.post(url+'/infra/subnet', data=json.dumps(data), headers=headers)


@app.route('/gateway', methods=['POST'])
def gateway():
    request_data = request.get_json()

    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'environment': get_environment(request_data),
        'vcn': request_data.get('vcn_data_might_be_more_things')
    }

    requests.post(url+'/infra/gateway', data=json.dumps(data), headers=headers)


@app.route('/images', methods=['POST'])
def images():
    request_data = request.get_json()

    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'user_id': request_data.get('user_id'),
        'os': request_data.get('operating_system'),
        'os_version': request_data.get('operating_system_version'),
        'shape': request_data.get('shape'),
        'environment': get_environment(request_data)
    }

    requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)


@app.route('/compute', methods=['POST'])
def compute():
    request_data = request.get_json()

    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'environment': get_environment(request_data),
        'user_id': request_data.get('user_id'),
        'ad': request_data.get('operating_system'),
        'compartment_id': request_data.get('operating_system_version'),
        'name': request_data.get('shape'),
        'image_id': request_data.get('shape'),
        'shape': request_data.get('shape'),
        # could get id and ad from subnet info
        'subnet_id': request_data.get('shape'),
        # todo: this is the vcn object. Find out what values are needed
        'vcn': request_data.get('shape')
    }

    r = requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)
    return r.json()


def get_environment(request_data):
    user_id = request_data.get('user_id')
    env_name = request_data.get('env_name')

    environment = Environment.query.join(
        User.environments
    ).filter(
        User.user_id == user_id,
        Environment.env_name == env_name
    ).first()

    return EnvironmentSchema(exclude=('id',)).dump(environment).data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
