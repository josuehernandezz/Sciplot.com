from flask import Flask, request, jsonify
import subprocess
import hmac
import hashlib
import os

app = Flask(__name__)

GITHUB_SECRET = 'your-github-webhook-secret'  # The secret you set in GitHub

# def verify_signature(payload_body, signature_header, secret_token):
#     """Verify the GitHub webhook signature to ensure it's from GitHub."""
#     if not signature_header:
#         raise ValueError("Signature header is missing!")

#     # Create the expected signature using HMAC and SHA256
#     hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
#     expected_signature = "sha256=" + hash_object.hexdigest()

#     # Compare the computed signature with the received signature
#     if not hmac.compare_digest(expected_signature, signature_header):
#         raise ValueError("Request signatures didn't match!")

#     return True

def verify_signature(payload_body, signature_header, secret_token):
    """Verify the GitHub webhook signature to ensure it's from GitHub."""
    if not signature_header:
        raise ValueError("Signature header is missing!")

    # Extract the 'sha256=' part of the signature header to get only the hash value
    if not signature_header.startswith("sha256="):
        raise ValueError("Invalid signature prefix in header!")

    # Get the actual hash value from the signature header (remove 'sha256=')
    signature_hash = signature_header[len("sha256="):]

    # Create the expected signature using HMAC and SHA256
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = hash_object.hexdigest()

    # Compare the computed signature with the received signature hash
    if not hmac.compare_digest(expected_signature, signature_hash):
        raise ValueError("Request signatures didn't match!")

    return True

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log all headers to inspect what’s being passed through
        print("Headers: ", request.headers)

        print("Pringing the header xhub signature-256", request.headers.get('X-Hub-Signature-256'))
        # Retrieve the signature from the headers
        signature = request.headers.get('X-Hub-Signature-256')
        print("Signature:", signature)
        if not signature:
            return jsonify({"error": "Missing signature"}), 400

        # Get the raw payload data
        payload = request.data
        print("THE PAYLOAD IS: payload", payload)

        # Verify the webhook signature using the new verify_signature function
        try:
            verify_signature(payload, signature, GITHUB_SECRET)
        except ValueError as e:
            return jsonify({"error": str(e)}), 403

        data = request.get_json(force=True)  # Explicitly parse JSON
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        if data.get('ref') == 'refs/heads/main' and data.get('repository', {}).get('name') == 'sciplot':  
            # Ensure it's the 'main' branch and the correct repository
            subprocess.run(["/home/josue/github-webhooks/deploy.sh"], check=True)
            return jsonify({"message": "Deployment triggered"}), 200

        return jsonify({"message": "No action taken"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)  # Run on port 9000
