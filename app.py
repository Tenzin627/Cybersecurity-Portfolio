"""
Flask application for the Personal Cybersecurity Portfolio.
"""

import os
import re
import secrets

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, render_template, request, session

import database
from services.hibp_service import HIBPServiceError, query_hibp_range

# Configuration

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "SECRET_KEY is not set. Create a .env file and add SECRET_KEY."
    )

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get("FLASK_ENV") == "production"
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# Database

database.init_db()


# CSRF Protection

@app.before_request
def ensure_csrf_token():
    """Create a CSRF token for the user's session."""

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)


@app.context_processor
def inject_csrf_token():
    """Make the CSRF token available to templates."""

    return {
        "csrf_token": session.get("csrf_token", "")
    }


def is_valid_csrf_token(submitted_token):
    """Check whether the submitted CSRF token is valid."""

    expected_token = session.get("csrf_token", "")

    if not expected_token:
        return False

    return secrets.compare_digest(
        expected_token,
        submitted_token or ""
    )


# Security Headers

@app.after_request
def set_security_headers(response):
    """Add basic security headers."""

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=()"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self'; "
        "img-src 'self' data:;"
    )

    return response


# Main Pages

@app.route("/")
def home():
    """Display the portfolio homepage."""

    return render_template("index.html")


@app.route("/projects")
def projects():
    """Display the projects page."""

    return render_template("projects.html")

@app.route("/projects/password-auditor")
def password_auditor():
    """Display the Personal Password Auditor."""

    return render_template("projects/password_auditor.html")


@app.route("/api/check/<prefix>")
def check_password(prefix):
    """Query HIBP using a 5-character SHA-1 hash prefix."""

    # Prefix must be exactly 5 hexadecimal characters.
    if not re.fullmatch(r"[0-9A-Fa-f]{5}", prefix):
        return jsonify({
            "error": "Invalid hash prefix."
        }), 400

    try:
        suffixes = query_hibp_range(prefix.upper())

        return jsonify({
            "suffixes": suffixes
        })

    except HIBPServiceError as error:
        return jsonify({
            "error": str(error)
        }), 502

@app.route("/certifications")
def certifications():
    """Display the certifications page."""

    return render_template("certifications.html")


# Contact Form

@app.route("/contact", methods=["POST"])
def contact():
    """Process the contact form."""

    # Check CSRF token
    submitted_token = request.form.get("csrf_token", "")

    if not is_valid_csrf_token(submitted_token):
        return jsonify({
            "success": False,
            "message": (
                "Security check failed. "
                "Please refresh the page and try again."
            )
        }), 400

    # Get form data
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    errors = []

    # Validate name
    if not name:
        errors.append("Name is required.")
    elif len(name) > 100:
        errors.append("Name must be under 100 characters.")

    # Validate email
    if not email:
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(email):
        errors.append("Please enter a valid email address.")

    # Validate message
    if not message:
        errors.append("Message is required.")
    elif len(message) > 2000:
        errors.append("Message must be under 2000 characters.")

    # Return validation errors
    if errors:
        return jsonify({
            "success": False,
            "message": " ".join(errors)
        }), 400

    # Save message
    try:
        database.insert_message(name, email, message)

    except Exception:
        app.logger.exception("Failed to save contact message")

        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again later."
        }), 500

    # Successful submission
    return jsonify({
        "success": True,
        "message": "Thanks for reaching out — I'll get back to you soon."
    })


# Error Handlers

@app.errorhandler(404)
def not_found(error):
    """Handle missing pages."""

    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """Handle unexpected server errors."""

    return jsonify({
        "success": False,
        "message": "An unexpected server error occurred."
    }), 500


# Run Application

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_ENV") != "production"

    app.run(debug=debug_mode)