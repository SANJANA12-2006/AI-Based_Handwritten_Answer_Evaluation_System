from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from models import db
from models.user import User
from models.class_model import Class


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/select-role")
def select_role():

    if current_user.is_authenticated:

        if current_user.role == "teacher":
            return redirect(url_for("teacher.dashboard"))

        return redirect(url_for("student.dashboard"))

    return render_template("auth/select_role.html")


@auth_bp.route("/register/<role>", methods=["GET", "POST"])
def register(role):

    if role not in ["teacher", "student"]:
        return redirect(url_for("auth.select_role"))

    if current_user.is_authenticated:

        if current_user.role == "teacher":
            return redirect(url_for("teacher.dashboard"))

        return redirect(url_for("student.dashboard"))

    classes = Class.query.order_by(Class.name).all()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        class_id = request.form.get("class_id")

        # -----------------------------
        # BASIC VALIDATION
        # -----------------------------

        if not name or not email or not password:

            flash(
                "Please fill in all required fields.",
                "error"
            )

            return render_template(
                "auth/register.html",
                role=role,
                classes=classes
            )

        # -----------------------------
        # PASSWORD VALIDATION
        # -----------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return render_template(
                "auth/register.html",
                role=role,
                classes=classes
            )

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return render_template(
                "auth/register.html",
                role=role,
                classes=classes
            )

        # -----------------------------
        # EMAIL CHECK
        # -----------------------------

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return render_template(
                "auth/register.html",
                role=role,
                classes=classes
            )

        # -----------------------------
        # STUDENT CLASS CHECK
        # -----------------------------

        if role == "student" and not class_id:

            flash(
                "Please select your class.",
                "error"
            )

            return render_template(
                "auth/register.html",
                role=role,
                classes=classes
            )

        # -----------------------------
        # CREATE USER
        # -----------------------------

        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role
        )

        # Assign class to student

        if role == "student":

            user.class_id = int(class_id)

        # Hash password

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        role=role,
        classes=classes
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "teacher":
            return redirect(
                url_for("teacher.dashboard")
            )

        return redirect(
            url_for("student.dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        selected_role = request.form.get(
            "role",
            ""
        ).strip().lower()

        # -----------------------------
        # FIND USER
        # -----------------------------

        user = User.query.filter_by(
            email=email
        ).first()

        # -----------------------------
        # CHECK LOGIN
        # -----------------------------

        if not user or not user.check_password(password):

            flash(
                "Invalid email or password.",
                "error"
            )

            return render_template(
                "auth/login.html",
                selected_role=selected_role
            )

        # -----------------------------
        # CHECK ROLE
        # -----------------------------

        if selected_role and user.role != selected_role:

            flash(
                f"This account is registered as a {user.role}.",
                "error"
            )

            return render_template(
                "auth/login.html",
                selected_role=selected_role
            )

        # -----------------------------
        # LOGIN
        # -----------------------------

        login_user(user)

        # -----------------------------
        # REDIRECT BY ROLE
        # -----------------------------

        if user.role == "teacher":

            return redirect(
                url_for("teacher.dashboard")
            )

        return redirect(
            url_for("student.dashboard")
        )

    return render_template(
        "auth/login.html",
        selected_role=""
    )


@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("main.home")
    )