from flask_app.app import db


class UserFunction(db.Model):
    """
    Model for the User Function association table
    """

    __tablename__ = 'user_function'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    function_id = db.Column(db.Integer, db.ForeignKey('functions.id'))