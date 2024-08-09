from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/tracker', methods=['GET'])
def tracker():
    user = request.args.get('user')
    doc = request.args.get('doc')
    app_name = request.args.get('app')
    version = request.headers.get('version')
    user_agent = request.headers.get('User-Agent')
    tracking_id = request.args.get('id')
    ip_address = request.remote_addr

    # Log for document opening.
    log = f"{doc} document opened by {user} {ip_address} tracking id {tracking_id} using {app_name} and version {version} useer agent: {user_agent} on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}\n"
    with open('track.log', 'a') as log_file:
        log_file.write(log)

    # Log for USB Drive Insertion.
    if tracking_id == "USBTracking":
        log_user_agent = f"USB Inserted by: {user_agent} on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}\n"
        with open('track.log', 'a') as log_file:
            log_file.write(log_user_agent)

    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)