from flask import flash, redirect, render_template, request, session

from src.services.auth_service import AuthService

# Controllers layer: maps HTTP requests to service calls.


def register_form():
    return render_template("register.html")


def register():
    try:
        user = AuthService.register(
            name=request.form["name"],
            university_id=request.form["universityId"],
            email=request.form["email"],
            password=request.form["password"],
            department=request.form["department"],
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect("/register")
    session["user_id"] = user.userId
    session["user_name"] = user.name
    session["role_name"] = user.role.roleName
    session["role"] = user.role.roleName
    flash("Account created successfully.", "success")
    return redirect("/dashboard")


def login_form():
    return render_template("login.html")


def login():
    try:
        user = AuthService.login(request.form["email"], request.form["password"])
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect("/login")
    session["user_id"] = user.userId
    session["user_name"] = user.name
    session["role_name"] = user.role.roleName
    session["role"] = user.role.roleName
    flash("Logged in successfully.", "success")
    return redirect("/dashboard")


def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect("/login")
