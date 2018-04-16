from flask_app.app import db


class User(db.Model):
    """
    Model for Users
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    environments = db.relationship('Environment', backref='users', secondary='user_environment')

    def __init__(self, user_id, environment):
        self.user_id = user_id
        self.environments.append(environment)