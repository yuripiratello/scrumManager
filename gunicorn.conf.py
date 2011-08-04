import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

user = "root" 
workers = numCPUs() * 2 + 1
bind = "0.0.0.0:8000"
pidfile = "/tmp/gunicorn-demo.pid"
backlog = 2048
logfile = "/etc/nginx/scrumManager/log/gunicorn.log"
loglevel = "info"
