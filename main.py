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

@app.route("/vms/list/active")
def list_active_doms():
    doms = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
    if doms == None:
        print("Fatal Error: Cannot List Domains!", file=sys.stderr)
        exit(1)
    return jsonify(doms)

@app.route("/vms/create")
def create_vms():
    return jsonify({
        "msg": "function not implemented yet"
    })

@app.route("/vms/<name>/uuid")
def get_dom_uuid(name):
    dom = conn.lookupByName(name)
    if dom == None:
        print("Fatal Error: Cannot Loop up Domain", file=sys.stderr)
        exit(1)
    return jsonify({
        "uuid": dom.UUIDString()
    })

@app.route("/vms/<name>/id")
def get_dom_id(name):
    dom = conn.lookupByName(name)
    if dom == None:
        print("Fatal Error: Cannot Loop up Domain", file=sys.stderr)
        exit(1)
    return jsonify({
        "id": dom.ID()
    })

@app.route("/vms/<name>/start")
def vm_start(id):
    dom = conn.lookupByName(name)
    if dom == None:
        print("Fatal Error: Cannot Look up Domain", file=sys.stderr)
        exit(1)
    if dom.create(dom) < 0:
        print('Fatal Error: Cannot boot Domain', file=sys.stderr)
        exit(1)
    return jsonify({
        "code": 200,
        "msg": "Domain Created!"
    })

if __name__ == '__main__':
    app.run(host='10.211.55.3', port=5050, debug=True)