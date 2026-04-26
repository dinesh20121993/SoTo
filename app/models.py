from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    sections = db.relationship("Section", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Section(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    goals = db.relationship("Goal", backref="section", lazy=True, cascade="all, delete-orphan")
    shopping_items = db.relationship("ShoppingItem", backref="section", lazy=True, cascade="all, delete-orphan")


class Goal(db.Model):
    __tablename__ = "goals"

    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3

    PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "High"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    priority = db.Column(db.Integer, default=PRIORITY_MEDIUM, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False)

    @property
    def priority_label(self):
        return self.PRIORITY_LABELS.get(self.priority, "Medium")


class ShoppingItem(db.Model):
    __tablename__ = "shopping_items"

    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3

    PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "High"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=True)
    priority = db.Column(db.Integer, default=PRIORITY_MEDIUM, nullable=False)
    is_purchased = db.Column(db.Boolean, default=False, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False)

    @property
    def priority_label(self):
        return self.PRIORITY_LABELS.get(self.priority, "Medium")
