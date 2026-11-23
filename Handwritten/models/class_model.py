from datetime import datetime

from models import db


class Class(db.Model):

    __tablename__ = "classes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    students = db.relationship(
        "User",
        backref="student_class",
        lazy=True
    )

    tests = db.relationship(
        "Test",
        backref="assigned_class",
        lazy=True
    )

    def __repr__(self):
        return f"<Class {self.name}>"