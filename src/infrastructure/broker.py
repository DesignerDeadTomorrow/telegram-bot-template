from taskiq import TaskiqScheduler
from taskiq.serializers import ORJSONSerializer
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from src.infrastructure.config import settings

broker_url = settings.redis.url

result_backend = RedisAsyncResultBackend(
    redis_url=broker_url,
    result_ex_time=3600,
)

broker = (
    ListQueueBroker(
        url=broker_url,
        queue_name="broker_queue",
    )
    .with_result_backend(result_backend=result_backend)
    .with_serializer(ORJSONSerializer())
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[RedisScheduleSource(url=broker_url)],
)
