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
    user_id = request.args.get('user_id')
    fingerprint = request.args.get('fingerprint')
    private_key = request.args.get('private_key')
    user_ocid = request.args.get('user_ocid')
    tenancy_ocid = request.args.get('tenancy_ocid')
    env_name = request.args.get('env_name')

    env = Environment(env_name, private_key, user_ocid, tenancy_ocid, fingerprint)
    user = User(user_id, env)

    # todo: more error handling for sql inserts

    db.session.add(user)
    db.session.commit()

    return json.dumps({'success': True, 'environment': env_name}), 200, headers


@app.route('/vcn')
def vcn():
    data = {
        'compartment_id': request.args.get('compartment_id'),
        'cidr_block': request.args.get('cidr_block'),
        'name': request.args.get('name'),
        'environment': get_environment(request)
    }

    requests.post(url+'/infra/vcn', data=json.dumps(data), headers=headers)


@app.route('/subnet')
def subnet():
    data = {
        'environment': get_environment(request),
        # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
        'vcn': request.args.get('vcn_data_might_be_more_things'),
        'ad': request.args.get('availability_domain')
    }

    requests.post(url+'/infra/subnet', data=json.dumps(data), headers=headers)


@app.route('/gateway')
def gateway():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'environment': get_environment(request),
        'vcn': request.args.get('vcn_data_might_be_more_things')
    }

    requests.post(url+'/infra/gateway', data=json.dumps(data), headers=headers)


@app.route('/images')
def images():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'user_id': request.args.get('user_id'),
        'os': request.args.get('operating_system'),
        'os_version': request.args.get('operating_system_version'),
        'shape': request.args.get('shape'),
        'environment': get_environment(request)
    }

    requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)


@app.route('/compute')
def compute():
    # todo: clean this up a bit to only pass what is necessary for the creation of the subnet
    data = {
        'environment': get_environment(request),
        'user_id': request.args.get('user_id'),
        'ad': request.args.get('operating_system'),
        'compartment_id': request.args.get('operating_system_version'),
        'name': request.args.get('shape'),
        'image_id': request.args.get('shape'),
        'shape': request.args.get('shape'),
        # could get id and ad from subnet info
        'subnet_id': request.args.get('shape'),
        # todo: this is the vcn object. Find out what values are needed
        'vcn': request.args.get('shape')
    }

    requests.post(url+'/infra/images', data=json.dumps(data), headers=headers)


def get_environment(request):
    user_id = request.args.get('user_id')
    env_name = request.args.get('env_name')

    environment = Environment.query.join(
        User
    ).filter(
        User.user_id == user_id,
        Environment.env_name == env_name
    ).first()

    return EnvironmentSchema().dump(environment).data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
