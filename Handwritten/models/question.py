from datetime import datetime

from models import db


class Question(db.Model):

    __tablename__ = "questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    test_id = db.Column(
        db.Integer,
        db.ForeignKey("tests.id"),
        nullable=False
    )

    question_number = db.Column(
        db.Integer,
        nullable=False
    )

    question_text = db.Column(
        db.Text,
        nullable=False
    )

    key_answer = db.Column(
        db.Text,
        nullable=False
    )

    source_type = db.Column(
        db.String(20),
        nullable=True,
        default="text"
    )

    source_filename = db.Column(
        db.String(255),
        nullable=True
    )

    source_path = db.Column(
        db.String(500),
        nullable=True
    )

    extracted_text = db.Column(
        db.Text,
        nullable=True
    )

    max_marks = db.Column(
        db.Float,
        nullable=False,
        default=1
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    evaluations = db.relationship(
        "Evaluation",
        backref="question",
        lazy=True
    )

    def __repr__(self):
        return f"<Question {self.question_number}>"