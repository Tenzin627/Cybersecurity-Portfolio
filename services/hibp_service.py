"""
services/hibp_service.py

Small helper module responsible for one thing: talking to the
HIBP Pwned Passwords "range" API.

This module never sees a password or a full hash - only a 5-character
hash prefix comes in, and it never logs that prefix anywhere.
"""

import requests

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"

# HIBP asks API consumers to identify their application via User-Agent.
# No API key is required for the free Pwned Passwords range endpoint.
HEADERS = {
    "User-Agent": "Personal-Password-Auditor-Portfolio-Project",
    "Add-Padding": "true",  # asks HIBP to pad responses, adding extra privacy
}

REQUEST_TIMEOUT_SECONDS = 6


class HIBPServiceError(Exception):
    """Raised whenever the HIBP request fails in a way the caller should handle."""


def query_hibp_range(prefix):
    """
    Query the HIBP Pwned Passwords range API for a given 5-character
    SHA-1 hash prefix and return the raw response body (a text block of
    "SUFFIX:COUNT" lines).

    Raises HIBPServiceError with a user-friendly message on any failure
    (network issue, timeout, non-200 response, rate limiting, etc.).
    """
    url = HIBP_RANGE_URL.format(prefix=prefix)

    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        raise HIBPServiceError("The breach-check service timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise HIBPServiceError("Could not reach the breach-check service. Check your connection.")
    except requests.exceptions.RequestException:
        raise HIBPServiceError("An unexpected network error occurred.")

    if response.status_code == 429:
        raise HIBPServiceError("Rate limit exceeded. Please wait a moment and try again.")

    if response.status_code != 200:
        raise HIBPServiceError(f"Breach-check service returned an unexpected status ({response.status_code}).")

    return response.text
