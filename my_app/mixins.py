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
    def get_id(cls, id):
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
        
    @classmethod
    def get_one_filtered_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).one_or_none()
            
    @classmethod
    def get_one_filtered_email(cls, email):
        return db.session.query(cls).filter(cls.email == email).one_or_none()
    
    @classmethod
    def get_one_filtered_userId(cls, user_id):
        return db.session.query(cls).filter(cls.user_id == user_id).one_or_none()
    
    @classmethod
    def get_order_by_userId(cls):
        return db.session.query(cls).order_by(cls.user_id.asc()).all()
    
    @classmethod
    def get_userId(cls, user_id):
        return db.session.query(cls).get(user_id)
    
    @classmethod
    def filter(cls, my_filter):
        return cls.query.filter(my_filter).all()
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)



from collections import OrderedDict
from sqlalchemy.engine.row import Row

class SerializableMixin():

    exclude_attr = []

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if key not in self.__class__.exclude_attr:
                result[key] = getattr(self, key)
        return result

    @staticmethod
    def to_dict_collection(collection):
        result = []
        for x in collection:  
            if isinstance(x, Row):
                obj = {}
                first = True
                for y in x:
                    if first:
                        # model
                        obj = y.to_dict()
                        first = False
                    else:
                        # relationships
                        key = y.__class__.__name__.lower()
                        del obj[key + '_id']
                        obj[key] = y.to_dict()
                result.append(obj)
            else:
                # only model
                result.append(x.to_dict())
        return result
