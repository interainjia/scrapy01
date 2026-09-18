import psycopg2


class PostgresPipeline:
    def __init__(self, host, port, dbname, user, password):
        self.conn_params = dict(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        return cls(
            host=s.get("POSTGRES_HOST"),
            port=s.getint("POSTGRES_PORT"),
            dbname=s.get("POSTGRES_DB"),
            user=s.get("POSTGRES_USER"),
            password=s.get("POSTGRES_PASSWORD"),
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(**self.conn_params)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """
            INSERT INTO quotes (text, author, tags, source_url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (text, author) DO NOTHING
            """,
            (
                item.get("text"),
                item.get("author"),
                item.get("tags"),
                item.get("source_url"),
            ),
        )
        self.conn.commit()
        return item
