import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware


class CoinsSpider(CrawlSpider):
    name = 'coins'
    allowed_domains = ['web.archive.org/web/20190101085451/https://coinmarketcap.com']
    start_urls = ['https://web.archive.org/web/20190101085451/https://coinmarketcap.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='currency-name-container link-secondary']"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'name': response.xpath("(//h1[@class='details-panel-item--name']/text())[2]").get(),
            'rank': response.xpath("label label-success").get(),
            'price(USD)': response.xpath("//span [@class = 'h2 text-semi-bold details-panel-item--price__value']/text()").get()
        }
