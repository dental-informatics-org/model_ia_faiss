from rq import Worker
from redis import Redis

redis_conn = Redis(host="localhost", port=6379)

if __name__ == "__main__":
    worker = Worker(queues=["default"], connection=redis_conn)
    worker.work()