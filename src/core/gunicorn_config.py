import multiprocessing

bind = ["0.0.0.0:80"]
daemon = True

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

loglevel = "debug"
accesslog = "/home/ubuntu/build/logs/access.log"
errorlog = "/home/ubuntu/build/logs/error.log"
