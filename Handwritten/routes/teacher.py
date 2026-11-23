import os
import re
import uuid
from datetime import datetime

import fitz

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
from models.class_model import Class
from models.test import Test
from models.question import Question
from models.submission import Submission
from models.evaluation import Evaluation, AnswerSheet
from services.image_processor import preprocess_image
from services.ocr_service import extract_handwritten_text


teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher"
)


def teacher_only():
    return (
        current_user.is_authenticated
        and current_user.role == "teacher"
    )


# ============================================================
# TEACHER DASHBOARD
# ============================================================

@teacher_bp.route("/dashboard")
@login_required
def dashboard():

    if not teacher_only():
        return "Access denied", 403

    total_tests = Test.query.filter_by(
        teacher_id=current_user.id
    ).count()

    total_students = 0

    for class_item in Class.query.all():
        total_students += len(class_item.students)

    published_tests = Test.query.filter_by(
        teacher_id=current_user.id,
        status="published"
    ).count()

    draft_tests = Test.query.filter_by(
        teacher_id=current_user.id,
        status="draft"
    ).count()

    return render_template(
        "teacher/dashboard.html",
        total_tests=total_tests,
        total_students=total_students,
        published_tests=published_tests,
        draft_tests=draft_tests
    )


# ============================================================
# TEACHER TESTS
# ============================================================

@teacher_bp.route("/tests")
@login_required
def tests():

    if not teacher_only():
        return "Access denied", 403

    tests = Test.query.filter_by(
        teacher_id=current_user.id
    ).order_by(
        Test.created_at.desc()
    ).all()

    return render_template(
        "teacher/tests.html",
        tests=tests
    )


@teacher_bp.route("/tests/<int:test_id>")
@login_required
def test_details(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    return render_template(
        "teacher/test_details.html",
        test=test
    )


# ============================================================
# CREATE TEST
# ============================================================

@teacher_bp.route(
    "/tests/create",
    methods=["GET", "POST"]
)
@login_required
def create_test():

    if not teacher_only():
        return "Access denied", 403

    classes = Class.query.order_by(
        Class.name
    ).all()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        class_id = request.form.get(
            "class_id"
        )

        duration = request.form.get(
            "duration"
        )

        if not title:

            flash(
                "Please enter a test title.",
                "error"
            )

            return render_template(
                "teacher/create_test.html",
                classes=classes
            )

        if not class_id:

            flash(
                "Please select a class.",
                "error"
            )

            return render_template(
                "teacher/create_test.html",
                classes=classes
            )

        selected_class = Class.query.get(
            int(class_id)
        )

        if not selected_class:

            flash(
                "Selected class does not exist.",
                "error"
            )

            return render_template(
                "teacher/create_test.html",
                classes=classes
            )

        test = Test(
            teacher_id=current_user.id,
            class_id=int(class_id),
            title=title,
            description=description,
            duration=int(duration)
            if duration else None,
            total_marks=0,
            status="draft"
        )

        db.session.add(test)
        db.session.commit()

        flash(
            "Test created. Now add your questions and key answers.",
            "success"
        )

        return redirect(
            url_for(
                "teacher.add_questions",
                test_id=test.id
            )
        )

    return render_template(
        "teacher/create_test.html",
        classes=classes
    )


# ============================================================
# ADD QUESTIONS
# ============================================================

ALLOWED_TEACHER_SOURCE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "pdf"
}


def allowed_teacher_source_file(filename):
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_TEACHER_SOURCE_EXTENSIONS


def extract_text_from_teacher_source(
    file_path,
    ocr_prompt=None,
    force_render=False
):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        doc = fitz.open(file_path)
        text_parts = []

        for page in doc:
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(page_text.strip())

        if text_parts and not force_render:
            doc.close()
            return "\n\n".join(text_parts)

        temp_images = []
        try:
            for page_index in range(len(doc)):
                page = doc[page_index]
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
                temp_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    "teacher_question_tmp",
                    f"pdf_page_{uuid.uuid4().hex}_{page_index}.jpg"
                )
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                pix.save(temp_path)
                temp_images.append(temp_path)

            extracted = []
            for image_path in temp_images:
                extracted.append(extract_handwritten_text(image_path, prompt=ocr_prompt))

            return "\n\n".join(part for part in extracted if part.strip())
        finally:
            for image_path in temp_images:
                try:
                    os.remove(image_path)
                except OSError:
                    pass

        return ""

    return extract_handwritten_text(file_path, prompt=ocr_prompt)


def split_question_and_answer(ocr_text):
    text = (ocr_text or "").strip()
    if not text:
        return "", ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    patterns = [
        r"(?is)(.*?)(?:\n\s*(?:key\s*answer|answer|solution|ans)\s*[:\-]?\s*)(.*)",
        r"(?is)(.*?)(?:\n\s*(?:question)\s*[:\-]?\s*)(.*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            left = match.group(1).strip()
            right = match.group(2).strip()
            if left and right:
                return left, right

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    if len(paragraphs) >= 2:
        question = paragraphs[0].strip()
        answer = "\n\n".join(paragraphs[1:]).strip()
        if question and answer:
            return question, answer

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) >= 2:
        question = "\n".join(lines[:-1]).strip()
        answer = lines[-1].strip()
        if question and answer:
            return question, answer

    return text, ""


def parse_numbered_document(text):
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()

    if not text:
        return {}

    number_pattern = re.compile(
        r"^\s*(?:q(?:uestion)?\s*)?(\d+)\s*[\.\):\-]?\s*(.*)$",
        re.IGNORECASE
    )
    blocks = {}
    current_number = None
    current_lines = []

    def save_block():
        if current_number is None:
            return
        block = "\n".join(current_lines).strip()
        if block:
            blocks[current_number] = block

    for line in text.split("\n"):
        line = line.strip()
        match = number_pattern.match(line)

        if match:
            save_block()
            current_number = int(match.group(1))
            current_lines = []
            if match.group(2).strip():
                current_lines.append(match.group(2).strip())
        elif current_number is not None and line:
            current_lines.append(line)

    save_block()
    return blocks


BULK_DOCUMENT_OCR_PROMPT = """
Read this handwritten document for bulk question import.
Return ONLY the visible content as plain text.
Each question or answer must start on its own line using this format:
1. content
2. content
3. content

Preserve the original numbering exactly when visible. Do not merge items.
Ignore notebook ruling lines, margins, stray marks, and decorative strokes.
Do not add explanations, summaries, or guessed content.
"""


@teacher_bp.route(
    "/tests/<int:test_id>/questions",
    methods=["GET", "POST"]
)
@login_required
def add_questions(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    if test.status == "published":

        flash(
            "Published tests cannot be modified.",
            "error"
        )

        return redirect(
            url_for("teacher.tests")
        )

    if request.method == "POST":

        question_text = request.form.get(
            "question_text",
            ""
        ).strip()

        key_answer = request.form.get(
            "key_answer",
            ""
        ).strip()

        max_marks = request.form.get(
            "max_marks",
            ""
        )

        question_file = request.files.get("question_source")
        answer_file = request.files.get("answer_source")

        source_type = "text"
        source_filename = None
        source_path = None
        extracted_text = None

        if question_file and question_file.filename:
            if not allowed_teacher_source_file(question_file.filename):
                flash(
                    "Only JPG, JPEG, PNG, WEBP, or PDF files are allowed for uploaded question sources.",
                    "error"
                )
                return redirect(
                    url_for(
                        "teacher.add_questions",
                        test_id=test.id
                    )
                )

            upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "teacher_questions"
            )
            os.makedirs(upload_folder, exist_ok=True)

            unique_id = uuid.uuid4().hex
            extension = question_file.filename.rsplit(".", 1)[1].lower()
            stored_filename = f"teacher_q_{test.id}_{unique_id}.{extension}"
            full_path = os.path.join(upload_folder, stored_filename)

            question_file.save(full_path)
            source_type = "image" if extension != "pdf" else "pdf"
            source_filename = question_file.filename
            source_path = full_path

            try:
                extracted_text = extract_text_from_teacher_source(full_path)
            except Exception as error:
                current_app.logger.exception(
                    "Teacher question OCR failed: %s",
                    error
                )
                extracted_text = None

            if extracted_text:
                parsed_question, parsed_answer = split_question_and_answer(extracted_text)
                if parsed_question and not question_text:
                    question_text = parsed_question
                if parsed_answer and not key_answer:
                    key_answer = parsed_answer

        if answer_file and answer_file.filename:
            if not allowed_teacher_source_file(answer_file.filename):
                flash(
                    "Only JPG, JPEG, PNG, WEBP, or PDF files are allowed for uploaded answer sources.",
                    "error"
                )
                return redirect(
                    url_for(
                        "teacher.add_questions",
                        test_id=test.id
                    )
                )

            upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "teacher_answers"
            )
            os.makedirs(upload_folder, exist_ok=True)

            unique_id = uuid.uuid4().hex
            extension = answer_file.filename.rsplit(".", 1)[1].lower()
            stored_filename = f"teacher_answer_{test.id}_{unique_id}.{extension}"
            full_path = os.path.join(upload_folder, stored_filename)

            answer_file.save(full_path)

            try:
                answer_text = extract_text_from_teacher_source(full_path)
            except Exception as error:
                current_app.logger.exception(
                    "Teacher answer OCR failed: %s",
                    error
                )
                answer_text = ""

            if answer_text:
                _, parsed_answer = split_question_and_answer(answer_text)
                if parsed_answer:
                    key_answer = parsed_answer
                elif not key_answer:
                    key_answer = answer_text.strip()

        if not question_text and not extracted_text:
            flash(
                "Please enter the question or upload a question image/PDF.",
                "error"
            )
            return redirect(
                url_for(
                    "teacher.add_questions",
                    test_id=test.id
                )
            )

        if not key_answer:
            flash(
                "Please enter the key answer or upload the answer image/PDF.",
                "error"
            )
            return redirect(
                url_for(
                    "teacher.add_questions",
                    test_id=test.id
                )
            )

        try:

            max_marks = float(max_marks)

            if max_marks <= 0:
                raise ValueError

        except (ValueError, TypeError):

            flash(
                "Marks must be a valid number greater than 0.",
                "error"
            )

            return redirect(
                url_for(
                    "teacher.add_questions",
                    test_id=test.id
                )
            )

        question_number = len(test.questions) + 1

        question = Question(
            test_id=test.id,
            question_number=question_number,
            question_text=question_text,
            key_answer=key_answer,
            source_type=source_type,
            source_filename=source_filename,
            source_path=source_path,
            extracted_text=extracted_text,
            max_marks=max_marks
        )

        db.session.add(question)

        test.total_marks = (
            float(test.total_marks or 0)
            + max_marks
        )

        db.session.commit()

        flash(
            f"Question {question_number} added successfully.",
            "success"
        )

        return redirect(
            url_for(
                "teacher.add_questions",
                test_id=test.id
            )
        )

    questions = Question.query.filter_by(
        test_id=test.id
    ).order_by(
        Question.question_number
    ).all()

    for question in questions:
        if question.source_path:
            question.source_url = "/uploads/" + os.path.relpath(
                question.source_path,
                current_app.config["UPLOAD_FOLDER"]
            ).replace(os.sep, "/")

    return render_template(
        "teacher/add_questions.html",
        test=test,
        questions=questions
    )


@teacher_bp.route(
    "/tests/<int:test_id>/questions/bulk",
    methods=["POST"]
)
@login_required
def add_questions_bulk(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    if test.status == "published":
        flash("Published tests cannot be modified.", "error")
        return redirect(url_for("teacher.tests"))

    question_file = request.files.get("bulk_question_paper")
    answer_file = request.files.get("bulk_answer_key")
    max_marks = request.form.get("bulk_max_marks", "").strip()

    if (
        not question_file
        or not question_file.filename
        or not answer_file
        or not answer_file.filename
    ):
        flash("Please upload both the question paper and answer key PDFs.", "error")
        return redirect(url_for("teacher.add_questions", test_id=test.id))

    if not question_file.filename.lower().endswith(".pdf") or not answer_file.filename.lower().endswith(".pdf"):
        flash("Bulk upload accepts PDF question papers and PDF answer keys only.", "error")
        return redirect(url_for("teacher.add_questions", test_id=test.id))

    try:
        marks = float(max_marks)
        if marks <= 0:
            raise ValueError
    except (TypeError, ValueError):
        flash("Default marks must be a valid number greater than 0.", "error")
        return redirect(url_for("teacher.add_questions", test_id=test.id))

    upload_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "teacher_bulk"
    )
    os.makedirs(upload_folder, exist_ok=True)

    unique_id = uuid.uuid4().hex
    question_filename = f"bulk_questions_{test.id}_{unique_id}.pdf"
    answer_filename = f"bulk_answers_{test.id}_{unique_id}.pdf"
    question_path = os.path.join(upload_folder, question_filename)
    answer_path = os.path.join(upload_folder, answer_filename)

    question_file.save(question_path)
    answer_file.save(answer_path)

    try:
        question_text = extract_text_from_teacher_source(
            question_path,
            ocr_prompt=BULK_DOCUMENT_OCR_PROMPT,
            force_render=True
        )
        answer_text = extract_text_from_teacher_source(
            answer_path,
            ocr_prompt=BULK_DOCUMENT_OCR_PROMPT,
            force_render=True
        )
        question_blocks = parse_numbered_document(question_text)
        answer_blocks = parse_numbered_document(answer_text)

        if not question_blocks or not answer_blocks:
            raise ValueError(
                "Could not detect numbered questions in one or both PDFs."
            )

        question_numbers = sorted(question_blocks)
        answer_numbers = sorted(answer_blocks)

        if set(question_numbers) != set(answer_numbers):
            if len(question_numbers) != len(answer_numbers):
                missing_answers = sorted(set(question_numbers) - set(answer_numbers))
                missing_questions = sorted(set(answer_numbers) - set(question_numbers))
                details = []
                if missing_answers:
                    details.append(f"missing answers for: {', '.join(map(str, missing_answers))}")
                if missing_questions:
                    details.append(f"answers without questions: {', '.join(map(str, missing_questions))}")
                raise ValueError(
                    "Question and answer numbers do not match ("
                    + "; ".join(details)
                    + ")."
                )

            # Handwritten OCR can misread a number while preserving the
            # document order. Pair equal-length documents by sequence.
            current_app.logger.warning(
                "Bulk OCR numbering mismatch; pairing %s blocks by document order.",
                len(question_numbers)
            )

        next_number = len(test.questions) + 1
        for offset, question_number in enumerate(question_numbers):
            answer_number = answer_numbers[offset]
            question = Question(
                test_id=test.id,
                question_number=next_number + offset,
                question_text=question_blocks[question_number],
                key_answer=answer_blocks[answer_number],
                source_type="pdf",
                source_filename=question_file.filename,
                source_path=question_path,
                extracted_text=question_blocks[question_number],
                max_marks=marks
            )
            db.session.add(question)

        test.total_marks = float(test.total_marks or 0) + (marks * len(question_numbers))
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        current_app.logger.exception("Bulk question import failed: %s", error)
        flash(f"Bulk import failed: {error}", "error")
        return redirect(url_for("teacher.add_questions", test_id=test.id))

    flash(f"Imported {len(question_numbers)} questions successfully.", "success")
    return redirect(url_for("teacher.add_questions", test_id=test.id))


# ============================================================
# PUBLISH TEST
# ============================================================

@teacher_bp.route(
    "/tests/<int:test_id>/publish",
    methods=["POST"]
)
@login_required
def publish_test(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    questions = Question.query.filter_by(
        test_id=test.id
    ).all()

    if not questions:

        flash(
            "You must add at least one question before publishing.",
            "error"
        )

        return redirect(
            url_for(
                "teacher.add_questions",
                test_id=test.id
            )
        )

    if test.total_marks <= 0:

        flash(
            "Test marks must be greater than zero.",
            "error"
        )

        return redirect(
            url_for(
                "teacher.add_questions",
                test_id=test.id
            )
        )

    test.status = "published"

    db.session.commit()

    flash(
        "Test published successfully. Students can now access it.",
        "success"
    )

    return redirect(
        url_for("teacher.tests")
    )


# ============================================================
# DELETE TEST
# ============================================================

@teacher_bp.route(
    "/tests/<int:test_id>/delete",
    methods=["POST"]
)
@login_required
def delete_test(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    if test.status == "published":

        flash(
            "Published tests cannot be deleted.",
            "error"
        )

        return redirect(
            url_for("teacher.tests")
        )

    db.session.delete(test)
    db.session.commit()

    flash(
        "Test deleted successfully.",
        "success"
    )

    return redirect(
        url_for("teacher.tests")
    )


# ============================================================
# VIEW TEST SUBMISSIONS
# ============================================================

@teacher_bp.route(
    "/tests/<int:test_id>/submissions"
)
@login_required
def submissions(test_id):

    if not teacher_only():
        return "Access denied", 403

    test = Test.query.filter_by(
        id=test_id,
        teacher_id=current_user.id
    ).first_or_404()

    submissions = Submission.query.filter_by(
        test_id=test.id
    ).order_by(
        Submission.submitted_at.desc()
    ).all()

    return render_template(
        "teacher/submissions.html",
        test=test,
        submissions=submissions
    )


# ============================================================
# VIEW INDIVIDUAL AI EVALUATION
# ============================================================

@teacher_bp.route(
    "/submissions/<int:submission_id>/evaluation"
)
@login_required
def evaluation(submission_id):

    if not teacher_only():
        return "Access denied", 403

    submission = Submission.query.get_or_404(
        submission_id
    )

    test = Test.query.filter_by(
        id=submission.test_id,
        teacher_id=current_user.id
    ).first()

    if not test:
        return "Access denied", 403

    evaluations = Evaluation.query.filter_by(
        submission_id=submission.id
    ).join(
        Question,
        Evaluation.question_id == Question.id
    ).order_by(
        Question.question_number
    ).all()

    for sheet in submission.answer_sheets:
        if sheet.original_path:
            sheet.image_url = "/uploads/" + os.path.relpath(
                sheet.original_path,
                current_app.config["UPLOAD_FOLDER"]
            ).replace(os.sep, "/")

    return render_template(
        "teacher/evaluation.html",
        submission=submission,
        test=test,
        evaluations=evaluations
    )


# ============================================================
# SAVE TEACHER REVIEW
# ============================================================

@teacher_bp.route(
    "/submissions/<int:submission_id>/evaluation/save",
    methods=["POST"]
)
@login_required
def save_evaluation(submission_id):

    if not teacher_only():
        return "Access denied", 403

    submission = Submission.query.get_or_404(
        submission_id
    )

    test = Test.query.filter_by(
        id=submission.test_id,
        teacher_id=current_user.id
    ).first()

    if not test:
        return "Access denied", 403

    evaluations = Evaluation.query.filter_by(
        submission_id=submission.id
    ).all()

    if not evaluations:

        flash(
            "No AI evaluation found for this submission.",
            "error"
        )

        return redirect(
            url_for(
                "teacher.submissions",
                test_id=test.id
            )
        )

    final_total = 0

    for evaluation in evaluations:

        marks_field = (
            f"marks_{evaluation.id}"
        )

        feedback_field = (
            f"feedback_{evaluation.id}"
        )

        marks_value = request.form.get(
            marks_field,
            ""
        ).strip()

        teacher_feedback = request.form.get(
            feedback_field,
            ""
        ).strip()

        try:

            teacher_marks = float(
                marks_value
            )

        except (ValueError, TypeError):

            teacher_marks = (
                evaluation.marks or 0
            )

        if teacher_marks < 0:
            teacher_marks = 0

        if teacher_marks > evaluation.max_marks:
            teacher_marks = evaluation.max_marks

        evaluation.teacher_marks = (
            teacher_marks
        )

        evaluation.teacher_feedback = (
            teacher_feedback
        )

        final_total += teacher_marks

    submission.total_marks = final_total

    if test.total_marks:

        submission.percentage = (
            final_total
            / float(test.total_marks)
        ) * 100

    submission.status = "teacher_reviewed"

    from datetime import datetime

    submission.evaluated_at = datetime.utcnow()

    db.session.commit()

    flash(
        "Teacher evaluation saved successfully.",
        "success"
    )

    return redirect(
        url_for(
            "teacher.evaluation",
            submission_id=submission.id
        )
    )