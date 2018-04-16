from sqlalchemy.exc import SQLAlchemyError

from flask_app.app import db
from flask_app.app.models import *


def recreate_db():
    try:
        db.reflect()
        db.drop_all()
    except SQLAlchemyError as e:
        raise ValueError(e)

    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    recreate_db()
