
from scrapy.spiders import SitemapSpider
from scrapy.utils.reactor import install_reactor

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

class EventsSpider(SitemapSpider):
    name = "events"
    allowed_domains = ["www.leuphana.de"]
    #start_urls = ["https://www.leuphana.de"]
    sitemap_urls = [
        "https://www.leuphana.de/sitemap.xml?sitemap=events&cHash=6e0af9fc4909858ff6f087b8acba2c2e"
    ]
    sitemap_rules = [
        ('/', 'parse_events')
    ]

    def parse_events(self, response):
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
c.crawl(EventsSpider)
c.start()