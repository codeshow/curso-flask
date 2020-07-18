from delivery.ext.auth.models import User
from delivery.ext.db import db


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        User(),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return User.query.all()
