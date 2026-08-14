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
