import multiprocessing

workers: int = multiprocessing.cpu_count() * 2 + 1
worker_class: str = "uvicorn.workers.UvicornWorker"

loglevel: str = "debug"
accesslog = "/home/build/logs/access_log"
errorlog = "/home/build/logs/error_log"
