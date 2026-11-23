from datetime import datetime

from models import db


class AnswerSheet(db.Model):

    __tablename__ = "answer_sheets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    submission_id = db.Column(
        db.Integer,
        db.ForeignKey("submissions.id"),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    stored_filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_path = db.Column(
        db.String(500),
        nullable=False
    )

    processed_path = db.Column(
        db.String(500),
        nullable=True
    )

    extracted_text = db.Column(
        db.Text,
        nullable=True
    )

    page_number = db.Column(
        db.Integer,
        nullable=False
    )

    processing_status = db.Column(
        db.String(30),
        default="uploaded"
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Evaluation(db.Model):

    __tablename__ = "evaluations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    submission_id = db.Column(
        db.Integer,
        db.ForeignKey("submissions.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False
    )

    student_answer = db.Column(
        db.Text,
        nullable=True
    )

    marks = db.Column(
        db.Float,
        nullable=True
    )

    max_marks = db.Column(
        db.Float,
        nullable=False
    )

    feedback = db.Column(
        db.Text,
        nullable=True
    )

    confidence = db.Column(
        db.Float,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="ai_evaluated"
    )

    teacher_marks = db.Column(
        db.Float,
        nullable=True
    )

    teacher_feedback = db.Column(
        db.Text,
        nullable=True
    )

    evaluated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )