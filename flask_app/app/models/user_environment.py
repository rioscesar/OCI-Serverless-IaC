from flask_app.app import db


class UserEnvironment(db.Model):
    """
    Model for the User Environment association table
    """

    __tablename__ = 'user_environment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    environment_id = db.Column(db.Integer, db.ForeignKey('environments.id'))