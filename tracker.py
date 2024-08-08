from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/tracker', methods=['GET'])
def tracker():
    user = request.args.get('user')
    doc = request.args.get('doc')
    app_name = request.args.get('app')
    version = request.headers.get('version')
    user_agent = request.headers.get('User-Agent', 'unknown')
    log = f"{doc} document opened by {user} using {app_name} and/or {user_agent} version {version} on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}\n"
    with open('track.log', 'a') as log_file:
        log_file.write(log)
    return 'OK', 200

if __name__ == '__main___':
    app.run(host='0.0.0.0', port=8000)