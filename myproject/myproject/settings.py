import os

BOT_NAME = "myproject"

SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 0.5

# --- Redis: distributed scheduler + dedup queue (scrapy-redis) ---
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"
SCHEDULER_PERSIST = True

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

# --- Item pipelines ---
ITEM_PIPELINES = {
    "scrapy_redis.pipelines.RedisPipeline": 300,
    "myproject.pipelines.PostgresPipeline": 400,
}

# --- PostgreSQL connection (used by PostgresPipeline) ---
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_DB = os.environ.get("POSTGRES_DB", "scrapy_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "scrapy_user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "scrapy_pass")

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
