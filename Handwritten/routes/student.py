import os
import uuid

import fitz

from services.image_processor import preprocess_image
from services.ocr_service import extract_handwritten_text

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user

from models import db
from models.test import Test
from models.submission import Submission
from models.evaluation import AnswerSheet


student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "pdf"
}


def student_only():

    return (
        current_user.is_authenticated
        and current_user.role == "student"
    )


def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


@student_bp.route("/dashboard")
@login_required
def dashboard():

    if not student_only():
        return "Access denied", 403

    available_tests = 0
    completed_tests = Submission.query.filter_by(
        student_id=current_user.id
    ).count()

    if current_user.class_id:

        available_tests = Test.query.filter_by(
            class_id=current_user.class_id,
            status="published"
        ).count()

    return render_template(
        "student/dashboard.html",
        available_tests=available_tests,
        completed_tests=completed_tests
    )


@student_bp.route("/tests")
@login_required
def tests():

    if not student_only():
        return "Access denied", 403

    if not current_user.class_id:

        return render_template(
            "student/tests.html",
            tests=[]
        )

    tests = Test.query.filter_by(
        class_id=current_user.class_id,
        status="published"
    ).order_by(
        Test.created_at.desc()
    ).all()

    return render_template(
        "student/tests.html",
        tests=tests
    )


@student_bp.route("/tests/<int:test_id>")
@login_required
def test_details(test_id):

    if not student_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        class_id=current_user.class_id,
        status="published"
    ).first_or_404()

    existing_submission = Submission.query.filter_by(
        test_id=test.id,
        student_id=current_user.id
    ).first()

    return render_template(
        "student/test_details.html",
        test=test,
        existing_submission=existing_submission
    )


@student_bp.route("/tests/<int:test_id>/upload")
@login_required
def upload_page(test_id):

    if not student_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        class_id=current_user.class_id,
        status="published"
    ).first_or_404()

    existing_submission = Submission.query.filter_by(
        test_id=test.id,
        student_id=current_user.id
    ).first()

    if existing_submission:

        flash(
            "You have already submitted this test.",
            "error"
        )

        return redirect(
            url_for(
                "student.test_details",
                test_id=test.id
            )
        )

    return render_template(
        "student/upload.html",
        test=test
    )


@student_bp.route(
    "/tests/<int:test_id>/upload",
    methods=["POST"]
)
@login_required
def upload_answers(test_id):

    if not student_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        class_id=current_user.class_id,
        status="published"
    ).first_or_404()

    existing_submission = Submission.query.filter_by(
        test_id=test.id,
        student_id=current_user.id
    ).first()

    if existing_submission:

        flash(
            "You have already submitted this test.",
            "error"
        )

        return redirect(
            url_for(
                "student.test_details",
                test_id=test.id
            )
        )

    files = request.files.getlist(
        "answer_sheets"
    )

    valid_files = []

    for file in files:

        if file and file.filename:

            if allowed_file(file.filename):

                valid_files.append(file)

    if not valid_files:

        flash(
            "Please upload at least one valid image or PDF.",
            "error"
        )

        return redirect(
            url_for(
                "student.upload_page",
                test_id=test.id
            )
        )


    # ------------------------------------------------
    # DIRECTORIES
    # ------------------------------------------------

    upload_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "answer_sheets"
    )

    processed_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "processed"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    os.makedirs(
        processed_folder,
        exist_ok=True
    )


    # ------------------------------------------------
    # CREATE SUBMISSION
    # ------------------------------------------------

    submission = Submission(
        test_id=test.id,
        student_id=current_user.id,
        status="processing"
    )

    db.session.add(submission)

    db.session.flush()


    try:

        # --------------------------------------------
        # PROCESS EVERY PAGE
        # --------------------------------------------

        page_number = 1

        for file in valid_files:

            original_filename = file.filename

            extension = (
                original_filename
                .rsplit(".", 1)[1]
                .lower()
            )


            unique_id = uuid.uuid4().hex


            original_filename_stored = (
                f"submission_{submission.id}_"
                f"{unique_id}."
                f"{extension}"
            )


            original_path = os.path.join(
                upload_folder,
                original_filename_stored
            )


            # ----------------------------------------
            # SAVE ORIGINAL IMAGE
            # ----------------------------------------

            file.save(
                original_path
            )


            page_sources = []

            if extension == "pdf":
                document = fitz.open(original_path)

                try:
                    for pdf_page_number in range(len(document)):
                        pdf_page = document[pdf_page_number]
                        pixmap = pdf_page.get_pixmap(
                            matrix=fitz.Matrix(2, 2),
                            alpha=False
                        )
                        page_filename = (
                            f"submission_{submission.id}_"
                            f"{unique_id}_page_{pdf_page_number + 1}.jpg"
                        )
                        page_path = os.path.join(
                            upload_folder,
                            page_filename
                        )
                        pixmap.save(page_path)
                        page_sources.append((
                            page_path,
                            f"{original_filename} - page {pdf_page_number + 1}",
                            page_filename
                        ))
                finally:
                    document.close()
            else:
                page_sources.append((
                    original_path,
                    original_filename,
                    original_filename_stored
                ))

            for page_path, page_filename, stored_filename in page_sources:
                processed_filename = (
                    f"submission_{submission.id}_"
                    f"{uuid.uuid4().hex}_processed.jpg"
                )
                processed_path = os.path.join(
                    processed_folder,
                    processed_filename
                )

                preprocess_image(
                    page_path,
                    processed_path
                )

                answer_sheet = AnswerSheet(
                    submission_id=submission.id,
                    original_filename=page_filename,
                    stored_filename=stored_filename,
                    original_path=page_path,
                    processed_path=processed_path,
                    extracted_text=None,
                    page_number=page_number,
                    processing_status="processing"
                )

                db.session.add(answer_sheet)
                db.session.flush()

                answer_sheet.extracted_text = extract_handwritten_text(
                    processed_path
                )
                answer_sheet.processing_status = "completed"

                db.session.commit()
                page_number += 1


        # --------------------------------------------
        # COMPLETE SUBMISSION
        # --------------------------------------------

        submission.status = "completed"

        db.session.commit()


    except Exception as error:

        db.session.rollback()

        current_app.logger.exception(
            "OCR processing failed: %s",
            error
        )

        # Mark submission as failed
        try:

            submission.status = "failed"

            db.session.commit()

        except Exception:

            db.session.rollback()


        flash(
            "The answer sheet was uploaded, "
            "but OCR processing failed. "
            "Please try again.",
            "error"
        )

        return redirect(
            url_for(
                "student.upload_page",
                test_id=test.id
            )
        )


    flash(
        "Answer sheets uploaded and processed successfully.",
        "success"
    )


    return redirect(
        url_for(
            "student.processing",
            submission_id=submission.id
        )
    )


@student_bp.route(
    "/processing/<int:submission_id>"
)
@login_required
def processing(submission_id):

    if not student_only():
        return "Access denied", 403

    submission = Submission.query.filter_by(
        id=submission_id,
        student_id=current_user.id
    ).first_or_404()

    return render_template(
        "student/processing.html",
        submission=submission
    )


@student_bp.route("/submission/<int:submission_id>/result")
@login_required
def result(submission_id):

    if not student_only():
        return "Access denied", 403

    submission = Submission.query.filter_by(
        id=submission_id,
        student_id=current_user.id
    ).first_or_404()

    return render_template(
        "student/result.html",
        submission=submission
    )