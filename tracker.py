from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Setup logging with rotation
log_handler = RotatingFileHandler('track.log', maxBytes=1500000000, backupCount=3)
log_handler.setFormatter(logging.Formatter('%(message)s'))
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


@app.route('/tracker', methods=['GET'])
def tracker():
    # Gathering request Data
    user = request.args.get('user', 'Unknown User')
    doc = request.args.get('doc', 'Unknown Document')
    app_name = request.args.get('app', 'Unknown Application')
    version = request.headers.get('version', 'Unknown Version')
    user_agent = request.headers.get('User-Agent', 'Unknown User-Agent')
    tracking_id = request.args.get('id', 'Unknown Tracking ID')
    ip_address = request.remote_addr or 'Unknown IP'
    headers = dict(request.headers)
    query_params = dict(request.args)
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')

    # Create a structured log entry
    log_entry = {
        "timestamp": timestamp,
        "ip_address": ip_address,
        "tracking_id": tracking_id,
        "user": user,
        "document": doc,
        "application": app_name,
        "application_version": version,
        "user_agent": user_agent,
        "headers": headers,
        "query_params": query_params
    }

    # Specific log entry for USB Tracking
    if tracking_id == "USBTracking":
        log_entry["event"] = "USB Insertion"
    else:
        log_entry["event"] = "Document Access"

    # Log the entry in JSON format
    app.logger.info(json.dumps(log_entry))

    return jsonify(status="success", message="Tracking logged"), 200


@app.route('/logs', methods=['GET'])
def view_logs():
    log_entries = []

    # Read and parse the log file
    try:
        with open('track.log', 'r') as log_file:
            for line in log_file:
                log_entries.append(json.loads(line))
    except FileNotFoundError:
        log_entries = [{"timestamp": "N/A", "event": "Log file not found", "details": "No logs available"}]

    # Render the logs in HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tracking Logs</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #e8ede6; margin: 0; padding: 20px; }
            h1 { text-align: center; }
            h4 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            tr:hover { background-color: #f5f5f5; }
        </style>
    </head>
    <body>
        <h1>ShadowUSB Tracking Logs:</h1>
        <h4>Below are the logs of users who inserted the Unknown/Untrusted USB or opened the Documents</h4>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Event</th>
                <th>User</th>
                <th>IP Address</th>
                <th>Application</th>
                <th>Version</th>
                <th>User Agent</th>
                <th>Details</th>
            </tr>
            {% for entry in log_entries %}
            <tr>
                <td>{{ entry.timestamp }}</td>
                <td>{{ entry.event }}</td>
                <td>{{ entry.user }}</td>
                <td>{{ entry.ip_address }}</td>
                <td>{{ entry.application }}</td>
                <td>{{ entry.application_version }}</td>
                <td>{{ entry.user_agent }}</td>
                <td>{{ entry.document }} {{ entry.query_params }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>      
    """

    return render_template_string(html_template, log_entries=log_entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)