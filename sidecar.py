from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def sidecar_download():
    data = request.get_json()
    filename = data.get('filename', 'default.txt')
    active_requests = data.get('active_requests', 'Unknown')  #read active_requests

    message = f"[SIDECAR SERVICE]: Successfully processed download for {filename}. Received active requests: {active_requests}"
    print(f"[INFO] {message}")

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)