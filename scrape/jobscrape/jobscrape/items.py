# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscrapeItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    experience = scrapy.Field()
    description = scrapy.Field()
    requirements = scrapy.Field()
    benefits = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    deadline = scrapy.Field()
