from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def import_models():
    from models.user import User
    from models.class_model import Class
    from models.test import Test
    from models.question import Question
    from models.submission import Submission
    from models.evaluation import AnswerSheet, Evaluation

    return (
        User,
        Class,
        Test,
        Question,
        Submission,
        AnswerSheet,
        Evaluation
    )