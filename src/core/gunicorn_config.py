import multiprocessing

workers: int = multiprocessing.cpu_count() * 2 + 1
worker_class: str = "uvicorn.workers.UvicornWorker"

loglevel: str = "debug"
accesslog = "/home/ubuntu/build/logs/access.log"
errorlog = "/home/ubuntu/build/logs/error.log"
