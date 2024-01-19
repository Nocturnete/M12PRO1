from . import db_manager as db, login_manager, mail_manager
from flask import current_app

class BaseMixin():

    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        return r.save()

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
    def get_all_join_by(cls, **kwargs):
        return db.session.query(cls).join(**kwargs).order_by(cls.id.asc()).all()

    @classmethod
    def get_with(cls, id, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_all_with(cls, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).order_by(cls.id.asc()).all()
    
    @classmethod
    def get_all_with_tree_classes(cls, join_cls, join_another_cls, id):
        return db.session.query(cls, join_cls, join_another_cls).join(join_cls).join(join_another_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_or_404(cls, id):
        return db.session.query(cls).get_or_404(id)
    
    @classmethod
    def get_order_by(cls):
        return db.session.query(cls).order_by(cls.id.asc()).all()
    
    @classmethod
    def get_order_by_banned(cls):
        return db.session.query(cls).order_by(cls.product_id.asc()).all()
    
    @classmethod
    def get_one_filtered(cls, id):
        return db.session.query(cls).filter(cls.id == id).one_or_none()