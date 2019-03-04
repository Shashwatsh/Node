from __future__ import print_function
from flask import Flask
from flask import jsonify
import libvirt
import sys


app = Flask(__name__)

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

@app.route("/ping")
def ping():
    hostname = conn.getHostname()
    if hostname == None:
        print("Fatal Error: Cannot get Hostname!", file=sys.stderr)
        exit(1)
    return "pong"

@app.route("/vms/list")
def list_vms():
    doms = conn.listDefinedDomains()
    if doms == None:
        print("Fatal Error: Cannot List Domains!", file=sys.stderr)
        exit(1)
    return jsonify(doms)

if __name__ == '__main__':
    app.run(host='10.211.55.3', port=5050, debug=True)