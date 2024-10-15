# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeuphanascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class NewsItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    topic = scrapy.Field()
    pub_year = scrapy.Field()
    pub_month = scrapy.Field()
    pub_day = scrapy.Field()

class EventsItem(scrapy.Item):
