from flask_app.app import db


class Function(db.Model):
    """
    Model for User Defined Functions
    """

    __tablename__ = 'functions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    private = db.Column(db.Boolean)

    # todo: might need to do a language field 

    def __init__(self, name, code):
        self.name = name
        self.code = code
