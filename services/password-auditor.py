"""
Personal Password Auditor - Flask Backend

This Flask app has two jobs only:
1. Serve the single-page front end (templates/index.html, static/*).
2. Proxy the k-anonymity range request to the HIBP Pwned Passwords API.

IMPORTANT - PRIVACY DESIGN:
The plaintext password NEVER reaches this backend. All SHA-1 hashing and
the final suffix comparison happen in the browser (see static/script.js).
The browser only ever sends this server the FIRST 5 CHARACTERS of a
SHA-1 hash (the "k-anonymity prefix"), which is not enough information
to recover or brute-force the original password.

Why route this through Flask instead of calling HIBP directly from the
browser? See the "Backend vs. Direct Browser Call" section in README.md
for the full tradeoff discussion. Short version: it lets us centralize
error handling, timeouts, and a proper User-Agent header in one place,
and keeps the door open for future protections (e.g. rate limiting)
without touching the frontend.
"""

import re
from flask import Flask, render_template, jsonify

from services.hibp_service import query_hibp_range, HIBPServiceError

app = Flask(__name__)

# HIBP hash prefixes are exactly 5 hexadecimal characters.
HASH_PREFIX_PATTERN = re.compile(r"^[0-9A-Fa-f]{5}$")


@app.route("/")
def index():
    """Serve the single-page application."""
    return render_template("index.html")


@app.route("/api/check/<prefix>", methods=["GET"])
def check_password_prefix(prefix):
    """
    Look up a SHA-1 hash prefix against the HIBP Pwned Passwords API.

    We only ever receive/handle a 5-character hash PREFIX here - never a
    password and never a full hash. This route never logs the prefix
    value itself into any long-lived store, and nothing about the
    request is persisted after the response is sent.
    """
    # Validate input strictly. This is the only user-controlled value
    # this backend ever touches, so we validate it before doing anything else.
    if not HASH_PREFIX_PATTERN.match(prefix):
        return jsonify({"error": "Invalid hash prefix format."}), 400

    try:
        suffixes_text = query_hibp_range(prefix.upper())
    except HIBPServiceError as exc:
        # Never leak stack traces or internal details to the client.
        return jsonify({"error": str(exc)}), 502

    return jsonify({"suffixes": suffixes_text})


if __name__ == "__main__":
    # debug=True is fine for local development/portfolio demos only.
    # Turn this off (or use a production WSGI server) for any real deployment.
    app.run(debug=True)
