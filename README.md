# Scrapy 分布式爬虫模板

Scrapy + Redis（分布式调度/去重）+ PostgreSQL（数据存储）+ Scrapyd（任务调度）的可运行模板。

## 目录结构

```
.
├── docker-compose.yml       # redis / postgres / scrapyd 三个服务
├── Dockerfile                # scrapyd 运行环境镜像
├── requirements.txt
├── scrapyd.conf               # scrapyd daemon 配置
├── init-db/01_init.sql        # 数据库初始化脚本（建表）
├── .env.example
└── myproject/                 # Scrapy 项目
    ├── scrapy.cfg              # 含 scrapyd-deploy 的部署配置
    └── myproject/
        ├── settings.py         # scrapy-redis 调度器/去重 + pipeline 配置
        ├── items.py
        ├── pipelines.py        # 写入 PostgreSQL
        └── spiders/example_spider.py  # RedisSpider 示例（爬 quotes.toscrape.com）
```

## 1. 启动基础设施（Redis + PostgreSQL + Scrapyd）

```bash
cp .env.example .env
docker compose up -d --build
```

- Redis: `localhost:6379`
- PostgreSQL: `localhost:5432`（首次启动会自动执行 `init-db/01_init.sql` 建表）
- Scrapyd: `http://localhost:6800`

## 2. 部署 Spider 到 Scrapyd

在宿主机（或任意能访问 6800 端口的机器）安装部署工具：

```bash
pip install scrapyd-client
```

进入项目目录并部署：

```bash
cd myproject
scrapyd-deploy local -p myproject
```

部署成功后可以确认：

```bash
curl http://localhost:6800/listprojects.json
curl http://localhost:6800/listspiders.json?project=myproject
```

## 3. 触发抓取

`example_spider.py` 是一个 `RedisSpider`，它会阻塞等待 Redis 中的起始 URL，然后再通过 scrapyd 调度运行：

```bash
# 先通过 scrapyd 调度任务（此时 spider 会启动并等待 Redis 队列）
curl http://localhost:6800/schedule.json -d project=myproject -d spider=quotes

# 再往 Redis 队列里塞一个起始 URL，触发实际抓取
docker compose exec redis redis-cli lpush quotes:start_urls "https://quotes.toscrape.com/"
```

多台机器 / 多个 scrapyd 实例都指向同一个 Redis，即可实现分布式抓取：请求队列与去重指纹集合都存在 Redis 里，天然支持横向扩容。

## 4. 查看抓取结果

```bash
docker compose exec postgres psql -U scrapy_user -d scrapy_db -c "SELECT * FROM quotes LIMIT 10;"
```

## 5. 常用 Scrapyd 任务管理命令

```bash
# 查看运行中/已完成的任务
curl http://localhost:6800/listjobs.json?project=myproject

# 取消任务
curl http://localhost:6800/cancel.json -d project=myproject -d job=<job_id>

# 删除项目某个版本
curl http://localhost:6800/delversion.json -d project=myproject -d version=<version>
```

## 本地开发调试（不经过 scrapyd）

```bash
pip install -r requirements.txt
cd myproject
export REDIS_URL=redis://localhost:6379/0
export POSTGRES_HOST=localhost
scrapy crawl quotes
```

## 扩展点

- 新增 Spider：在 `myproject/myproject/spiders/` 下继承 `scrapy_redis.spiders.RedisSpider`（或 `RedisCrawlSpider`），设置唯一的 `redis_key`。
- 新增数据表/字段：修改 `init-db/01_init.sql`，并在 `pipelines.py` 中同步调整写入逻辑。
- 定时调度：可用 `curl schedule.json` 配合 crontab，或引入 `scrapydweb` 做可视化管理（未包含在本模板中）。
