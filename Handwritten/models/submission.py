from datetime import datetime

from models import db


class Submission(db.Model):

    __tablename__ = "submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    test_id = db.Column(
        db.Integer,
        db.ForeignKey("tests.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total_marks = db.Column(
        db.Float,
        nullable=True
    )

    percentage = db.Column(
        db.Float,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="submitted"
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    evaluated_at = db.Column(
        db.DateTime,
        nullable=True
    )

    answer_sheets = db.relationship(
        "AnswerSheet",
        backref="submission",
        lazy=True,
        cascade="all, delete-orphan"
    )

    evaluations = db.relationship(
        "Evaluation",
        backref="submission",
        lazy=True,
        cascade="all, delete-orphan"
    )

    student = db.relationship(
        "User",
        foreign_keys=[student_id],
        backref="submissions"
    )

    def __repr__(self):
        return f"<Submission {self.id}>"