from . import db_manager as db, login_manager, mail_manager
from flask import current_app

class BaseMixin():

    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        return r.save()

    def update(self):
        return self.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def get(cls, id):
        current_app.logger.debug(cls)
        return db.session.query(cls).get(id)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_filtered_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def get_all_filtered_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).order_by(cls.id.asc()).all()

    @classmethod
    def get_with(cls, id, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_all_with(cls, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).order_by(cls.id.asc()).all()
    
    @classmethod
    def get_or_404(cls, id):
        return db.session.query(cls).get_or_404(id)