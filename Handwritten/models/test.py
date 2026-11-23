from datetime import datetime

from models import db


class Test(db.Model):

    __tablename__ = "tests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    duration = db.Column(
        db.Integer,
        nullable=True
    )

    total_marks = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="draft"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    questions = db.relationship(
        "Question",
        backref="test",
        lazy=True,
        cascade="all, delete-orphan"
    )

    submissions = db.relationship(
        "Submission",
        backref="test",
        lazy=True,
        cascade="all, delete-orphan"
    )

    teacher = db.relationship(
        "User",
        foreign_keys=[teacher_id],
        backref="created_tests"
    )

    def __repr__(self):
        return f"<Test {self.title}>"