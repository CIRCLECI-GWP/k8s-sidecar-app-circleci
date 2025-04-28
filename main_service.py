from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

SIDECARS = [
    "http://sidecar-service:5000"
]

THRESHOLD = 30

@app.route('/download', methods=['POST'])
def download_file():
    # Generate a random number between 0 and 50
    random_requests = random.randint(0, 50)
    
    # Print the number of active requests in normal text
    print(f"[INFO] Active Requests: {random_requests}")

    if random_requests > THRESHOLD:
        # Forward the request to a random sidecar
        sidecar_url = random.choice(SIDECARS)
        print(f"[INFO] Routing request to sidecar: {sidecar_url}")
        try:
            # Send both the original request + active_requests
            data = request.get_json()
            payload = dict(data or {})
            payload["active_requests"] = random_requests  # 👈 Add the number to the request

            response = requests.post(f"{sidecar_url}/download", json=payload)
            return (response.content, response.status_code, response.headers.items())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Process download directly
        data = request.get_json()
        filename = data.get('filename', 'default.txt')
        content = f"[MAIN SERVICE]: Successfully processed download for {filename}. Number of active requests is {random_requests}"
        return jsonify({"message": content})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
