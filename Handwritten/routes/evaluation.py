from flask import (
    Blueprint,
    jsonify,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models.submission import Submission
from services.evaluation_engine import evaluate_submission


evaluation_bp = Blueprint(
    "evaluation",
    __name__,
    url_prefix="/evaluation"
)


@evaluation_bp.route(
    "/<int:submission_id>/evaluate",
    methods=["POST"]
)
@login_required
def evaluate(submission_id):

    if not current_user.is_authenticated:
        return jsonify({
            "success": False,
            "message": "Authentication required."
        }), 401

    submission = Submission.query.filter_by(
        id=submission_id,
        student_id=current_user.id
    ).first()

    if not submission:

        return jsonify({
            "success": False,
            "message": "Submission not found."
        }), 404

    try:

        # If already evaluated, don't evaluate again.
        if submission.status == "evaluated":

            return jsonify({
                "success": True,
                "already_evaluated": True,
                "redirect_url": url_for(
                    "student.result",
                    submission_id=submission.id
                )
            })

        result = evaluate_submission(
            submission.id
        )

        return jsonify({
            "success": True,
            "already_evaluated": False,
            "total_marks": result["total_marks"],
            "max_marks": result["max_marks"],
            "percentage": result["percentage"],
            "redirect_url": url_for(
                "student.result",
                submission_id=submission.id
            )
        })

    except Exception as error:

        print(
            "Evaluation Error:",
            error
        )

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500