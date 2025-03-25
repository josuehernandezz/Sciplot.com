from flask import Flask, request, jsonify
import json
import subprocess
import hmac
import hashlib

app = Flask(__name__)

repository_name = 'Sciplot.com'
script_path = "/home/josue/sciplot/github-webhooks/deploy.sh"
GITHUB_SECRET = 'your-github-webhook-secret'  # The secret you set in GitHub

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
        signature = request.headers.get('X-Hub-Signature-256')
        print(request.headers)
        print("Payload: ")
        print(request.data)  # This is where you can access the raw payload
        if not signature:
            return jsonify({"error": "Missing signature"}), 400

        # Get the raw payload data
        payload = request.data

        # Verify the webhook signature using the new verify_signature function
        try:
            verify_signature(payload, signature, GITHUB_SECRET)
        except ValueError as e:
            return jsonify({"error": str(e)}), 403
        
        # Decode the payload from raw byte string to a Python dictionary
        payload_data = json.loads(request.data.decode('utf-8'))  # Decoding byte string to a dict

        # Extract relevant data from the payload
        ref = payload_data.get('ref')
        repo_name = payload_data.get('repository', {}).get('name')

        print(f"ref: {ref}")
        print(f"Repository: {repo_name}")

        # Check if the push was to the 'main' branch and the correct repository
        if ref == 'refs/heads/main' and repo_name == repository_name:
            subprocess.run([script_path], check=True)
            return jsonify({"message": "Deployment triggered"}), 200

        return jsonify({"message": "No action taken"}), 400

    except Exception as e:
        print("The error is:")
        print(e)
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)  # Run on port 9000
