import hashlib
import os

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/ebay/account-deletion")
def ebay_challenge():
    challenge_code = request.args.get("challenge_code", "")
    verification_token = os.environ.get("EBAY_VERIFICATION_TOKEN", "")
    endpoint = os.environ.get("EBAY_NOTIFICATION_ENDPOINT", "")

    if not challenge_code:
        return jsonify({"error": "missing challenge_code"}), 400

    if not verification_token or not endpoint:
        return jsonify({"error": "webhook is not configured"}), 500

    challenge_response = hashlib.sha256(
        (challenge_code + verification_token + endpoint).encode("utf-8")
    ).hexdigest()

    return jsonify({"challengeResponse": challenge_response}), 200


@app.post("/ebay/account-deletion")
def ebay_notification():
    # Acknowledge receipt promptly.
    # Notification verification/deletion processing will be added
    # before this endpoint is considered fully production-complete.
    request.get_json(silent=True)
    return "", 204
@app.get("/privacy")
def privacy():
    return """
    <!doctype html>
    <html>
    <head>
        <title>Maryam Resale Agent - Privacy Policy</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6;">
        <h1>Privacy Policy</h1>
        <p><strong>Maryam Resale Agent</strong></p>

        <p>Maryam Resale Agent uses information authorized through eBay
        to provide resale and listing-related functionality.</p>

        <p>Information obtained through eBay is used only as necessary
        to operate the application and provide its services.</p>

        <p>Maryam Resale Agent does not sell personal information.</p>

        <p>Data may be processed or stored only as necessary to operate,
        maintain, secure, and improve the application and to comply with
        applicable requirements.</p>

        <p>Users may revoke the application's access to their eBay
        account through their eBay account settings.</p>

        <p>Last updated: August 2026</p>
    </body>
    </html>
    """, 200
