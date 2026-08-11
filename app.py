"""
Flask application entry point for the Cybersecurity Portfolio website.

This file wires together configuration, routes, and the SQLite database.
Keep this file focused on request handling — database work lives in database.py.
"""

import os
import re
import secrets

from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv

import database

# Load variables from .env into the environment before anything reads them.
load_dotenv()

app = Flask(__name__)

# SECRET_KEY is required for signing the session cookie (used for CSRF tokens).
# Fail loudly in production if it was never set, instead of silently using
# an insecure default.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "SECRET_KEY is not set. Copy .env.example to .env and set a real value."
    )

# Only trust cookies over HTTPS once we're actually deployed. This is safe to
# leave True locally too, since most browsers still allow it over localhost.
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") == "production"

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.before_request
def ensure_csrf_token():
    """Make sure every session has a CSRF token before rendering a form."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)


@app.context_processor
def inject_csrf_token():
    """Expose the CSRF token to every template as {{ csrf_token }}."""
    return {"csrf_token": session.get("csrf_token", "")}


@app.after_request
def set_security_headers(response):
    """Attach baseline security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self'; "
        "img-src 'self' data:;"
    )
    return response


def is_valid_csrf_token(submitted_token):
    """Compare the submitted token to the one stored in the session."""
    expected_token = session.get("csrf_token", "")
    return bool(expected_token) and secrets.compare_digest(expected_token, submitted_token or "")


@app.route("/")
def home():
    """Render the single-page portfolio."""
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    """
    Handle contact form submissions.

    Validates every field server-side (never trust the client), checks the
    CSRF token, and stores the message using a parameterized query.
    """
    submitted_token = request.form.get("csrf_token", "")
    if not is_valid_csrf_token(submitted_token):
        return jsonify({"success": False, "message": "Security check failed. Please refresh and try again."}), 400

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    errors = []
    if not name:
        errors.append("Name is required.")
    elif len(name) > 100:
        errors.append("Name must be under 100 characters.")

    if not email:
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(email):
        errors.append("Please enter a valid email address.")

    if not message:
        errors.append("Message is required.")
    elif len(message) > 2000:
        errors.append("Message must be under 2000 characters.")

    if errors:
        return jsonify({"success": False, "message": " ".join(errors)}), 400

    try:
        database.insert_message(name, email, message)
    except Exception:
        # Never leak internal error details (stack traces, SQL, file paths)
        # back to the client.
        app.logger.exception("Failed to save contact message")
        return jsonify({"success": False, "message": "Something went wrong. Please try again later."}), 500

    return jsonify({"success": True, "message": "Thanks for reaching out — I'll get back to you soon."})


@app.errorhandler(404)
def not_found(_error):
    return render_template("index.html"), 404


@app.errorhandler(500)
def server_error(_error):
    # Generic message only — details go to the server log, not the response.
    return jsonify({"success": False, "message": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    database.init_db()
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug_mode)
