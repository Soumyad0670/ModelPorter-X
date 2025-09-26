# gunicorn.conf.py
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
loglevel = 'info'
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'

# Process naming
proc_name = 'ml_model_api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
# keyfile = None
# certfile = None