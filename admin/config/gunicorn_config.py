bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
timeout = 240
workers = 1
loglevel = "debug"