from datetime import datetime

from models import db
from models.test import Test
from models.question import Question
from models.submission import Submission
from models.evaluation import Evaluation, AnswerSheet

from services.answer_parser import parse_answers
from services.ai_evaluator import evaluate_answer


def get_submission_text(submission_id):
    """
    Collect OCR text from all answer-sheet pages
    belonging to a submission.
    """

    sheets = (
        AnswerSheet.query
        .filter_by(submission_id=submission_id)
        .order_by(AnswerSheet.page_number.asc())
        .all()
    )

    if not sheets:
        return ""

    page_texts = []

    for sheet in sheets:

        if sheet.extracted_text:
            page_texts.append(
                sheet.extracted_text.strip()
            )

    return "\n\n".join(page_texts)


def evaluate_submission(submission_id):
    """
    Evaluate one complete student submission.

    Flow:

    Submission
        ↓
    OCR text
        ↓
    Parse answers
        ↓
    Get teacher questions
        ↓
    Evaluate every answer
        ↓
    Save evaluations
        ↓
    Calculate total marks
    """

    submission = Submission.query.get(
        submission_id
    )

    if not submission:
        raise ValueError(
            "Submission not found."
        )

    test = Test.query.get(
        submission.test_id
    )

    if not test:
        raise ValueError(
            "Test not found."
        )

    questions = (
        Question.query
        .filter_by(test_id=test.id)
        .order_by(
            Question.question_number.asc()
        )
        .all()
    )

    if not questions:
        raise ValueError(
            "No questions found for this test."
        )

    extracted_text = get_submission_text(
        submission.id
    )

    if not extracted_text.strip():
        raise ValueError(
            "No OCR text found for this submission."
        )

    expected_question_numbers = [
        question.question_number
        for question in questions
    ]

    student_answers = parse_answers(
        extracted_text,
        expected_numbers=expected_question_numbers
    )

    if not student_answers:
        raise ValueError(
            "Could not detect numbered answers "
            "from the OCR text."
        )

    # Remove previous AI evaluations for this
    # submission so that re-evaluation does not
    # create duplicate records.
    Evaluation.query.filter_by(
        submission_id=submission.id
    ).delete(
        synchronize_session=False
    )

    db.session.flush()

    total_marks = 0.0
    total_max_marks = 0.0

    evaluation_results = []

    for question in questions:

        question_number = (
            question.question_number
        )

        student_answer = student_answers.get(
            question_number,
            ""
        )

        max_marks = float(
            question.max_marks or 0
        )

        total_max_marks += max_marks

        if student_answer.strip():

            result = evaluate_answer(
                student_answer=student_answer,
                key_answer=question.key_answer,
                max_marks=max_marks
            )

        else:

            result = {
                "marks": 0,
                "percentage": 0,
                "semantic_score": 0,
                "keyword_score": 0,
                "text_match_score": 0,
                "feedback": (
                    "No answer was detected "
                    "for this question."
                )
            }

        marks = float(
            result["marks"]
        )

        total_marks += marks

        evaluation = Evaluation(
            submission_id=submission.id,
            question_id=question.id,
            student_answer=student_answer,
            marks=marks,
            max_marks=max_marks,
            feedback=result["feedback"],
            confidence=result["percentage"],
            status="ai_evaluated",
            evaluated_at=datetime.utcnow()
        )

        db.session.add(
            evaluation
        )

        evaluation_results.append({
            "question_id": question.id,
            "question_number": question_number,
            "question_text": question.question_text,
            "student_answer": student_answer,
            "key_answer": question.key_answer,
            "marks": marks,
            "max_marks": max_marks,
            "percentage": result["percentage"],
            "semantic_score": result["semantic_score"],
            "keyword_score": result["keyword_score"],
            "text_match_score": result["text_match_score"],
            "feedback": result["feedback"]
        })

    if total_max_marks > 0:

        percentage = (
            total_marks /
            total_max_marks
        ) * 100

    else:

        percentage = 0

    submission.total_marks = round(
        total_marks,
        2
    )

    submission.percentage = round(
        percentage,
        2
    )

    submission.status = "evaluated"

    submission.evaluated_at = (
        datetime.utcnow()
    )

    db.session.commit()

    return {
        "submission_id": submission.id,
        "test_id": test.id,
        "student_id": submission.student_id,
        "total_marks": round(
            total_marks,
            2
        ),
        "max_marks": round(
            total_max_marks,
            2
        ),
        "percentage": round(
            percentage,
            2
        ),
        "evaluations": evaluation_results
    }