from flask import Flask, request
from datetime import datetime
import pytz
import os
import subprocess

app = Flask(__name__)

LOG_FILE = "/home/ubuntu/keepalive/keepalive.log"

@app.route('/ping', methods=['GET'])
def ping():
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "")
    query = request.query_string.decode()
    
    msg = f"[{now}] IP={ip} UA=\"{ua}\" QUERY=\"{query}\"\n"

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(msg)

    _ = sum(i * i for i in range(10000))

    return f"Keepalive OK - {now}\n"

@app.route('/push', methods=['GET', 'POST'])
def push_to_git():

    cmd = "cd /home/ubuntu/keepalive && git add keepalive.log && git commit -m 'Auto update' && git push origin main"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

