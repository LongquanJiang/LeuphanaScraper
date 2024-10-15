from scrapy.spiders import SitemapSpider
from scrapy.utils.reactor import install_reactor

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

class PagesSpider(SitemapSpider):
    name = "pages"
    allowed_domains = ["www.leuphana.de"]
    sitemap_urls = [
        "https://www.leuphana.de/sitemap.xml?sitemap=pages&cHash=0b181867b3901c1e7699ac903a3a1784"
    ]
    sitemap_rules = [
        ('leuphana', 'parse_article')
    ]

    def parse_article(self, response):
        print("parse_article url: ", response.url)

        yield {"url": response.url}

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess(
    settings={
        'USER_AGENT': 'Mozilla/5.0',
        # save in file as CSV, JSON or XML
        'FEED_FORMAT': 'csv',     # csv, json, xml
        'FEED_URI': 'output.csv', #
        "TWISTED_REACTOR" : 'asyncio'
    }
)
c.crawl(PagesSpider)
c.start()