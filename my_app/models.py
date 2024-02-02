from flask_login import UserMixin
from . import db_manager as db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash
from .mixins import BaseMixin, SerializableMixin
from datetime import timedelta, timezone, datetime
import secrets

class User(db.Model, BaseMixin, UserMixin, SerializableMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    __password = db.Column("password", db.String, nullable=False)
    verified = db.Column(db.Integer, nullable=False)
    email_token = db.Column(db.String, nullable=True, server_default=None)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    blocked_user = relationship('BlockedUser', back_populates='user', uselist=False)
    token = db.Column(db.String, unique=True, nullable=True)
    token_expiration = db.Column(db.DateTime, nullable=True)

    exclude_attr = ['password']

    def get_id(self):
        return self.email

    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(
                tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(
            seconds=1)
        self.save()
        
    @staticmethod
    def check_token(token):
        user = User.get_filtered_by(token=token)
        if user is None or user.token_expiration.replace(
                tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user

    def get_id(self):
        return self.email
    
    @hybrid_property
    def password(self):
        return "No password"
    
    @password.setter
    def password(self, plain_text_password):
        self.__password = generate_password_hash(plain_text_password, method="scrypt")

    def check_password(self, some_password):
        return check_password_hash(self.__password, some_password)

    def is_admin(self):
        return self.role == "admin"

    def is_moderator(self):
        return self.role == "moderator"
    
    def is_admin_or_moderator(self):
        return self.is_admin() or self.is_moderator()
    
    def is_wanner(self):
        return self.role == "wanner"

    def is_action_allowed_to_product(self, action, product = None):
        from .helper_role import _permissions, Action

        current_permissions = _permissions[self.role]
        if not current_permissions:
            return False
        
        if not action in current_permissions:
            return False
        
        # Un usuari wanner sols pot modificar el seu propi producte
        if (action == Action.products_update and self.is_wanner()):
            if not product:
                return False
            return self.id == product.seller_id
        
        # Un usuari wanner sols pot eliminar el seu propi producte
        if (action == Action.products_delete and self.is_wanner()):
            if not product:
                return False
            return self.id == product.seller_id
        
        # si hem arribat fins aquí, l'usuari té permisos
        return True

class Product(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Category(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class Status(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class BlockedUser(db.Model, BaseMixin):
    __tablename__ = "blocked_users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    reason = db.Column(db.String)
    user = relationship('User', back_populates='blocked_user')

class Banned_Products(db.Model, BaseMixin):
    __tablename__ = "banned_products"
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    reason = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())

class Order(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    offer = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())
    
    product = relationship("Product", back_populates="orders")
    buyer = relationship("User", back_populates="orders")
    
    __table_args__ = (
        db.UniqueConstraint("product_id", "buyer_id", name="uc_product_buyer"),
    )

class ConfirmedOrder(db.Model, BaseMixin):
    __tablename__ = "confirmed_orders"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())
    
    order = relationship("Order", back_populates="confirmed_order")


User.orders = relationship("Order", back_populates="buyer", uselist=True)
Product.orders = relationship("Order", back_populates="product", uselist=True)

Order.confirmed_order = relationship("ConfirmedOrder", back_populates="order", uselist=False)
ConfirmedOrder.order = relationship("Order", back_populates="confirmed_order", uselist=False)
