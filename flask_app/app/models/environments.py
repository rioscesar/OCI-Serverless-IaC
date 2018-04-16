from flask_app.app import db


class Environment(db.Model):
    """
    Model for User Environments
    """

    __tablename__ = 'environments'

    id = db.Column(db.Integer, primary_key=True)
    env_name = db.Column(db.String, unique=True)

    private_key = db.Column(db.String)
    user_ocid = db.Column(db.String)
    tenancy_ocid = db.Column(db.String)
    fingerprint = db.Column(db.String)
    region = db.Column(db.String)

    def __init__(self, env_name, private_key, user_ocid, tenancy_ocid, fingerprint, region):
        self.env_name = env_name
        self.private_key = private_key
        self.user_ocid = user_ocid
        self.tenancy_ocid = tenancy_ocid
        self.fingerprint = fingerprint
        self.region = region
