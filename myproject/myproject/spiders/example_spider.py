from scrapy_redis.spiders import RedisSpider

from myproject.items import QuoteItem


class QuotesSpider(RedisSpider):
    """
    Distributed spider driven by a Redis list.

    Push a start URL to trigger a crawl:
        redis-cli lpush quotes:start_urls "https://quotes.toscrape.com/"
    """

    name = "quotes"
    redis_key = "quotes:start_urls"

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            item["source_url"] = response.url
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
