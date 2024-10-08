import scrapy


class TopcvSpider(scrapy.Spider):
    name = "topcv"
    allowed_domains = ["topcv.vn"]
    start_urls = ["https://www.topcv.vn/viec-lam-it?page=1"]
    page_limit = 2

    def parse(self, response):
        # Extract the items on the page
        product_links = response.xpath(
            '//div[contains(@class, "job-item-2")]//h3[contains(@class, "title")]//a//@href'
        ).getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_item)

        # Handle pagination
        current_page = int(response.url.split("page=")[-1])
        if current_page < self.page_limit:
            next_page = current_page + 1
            next_page_url = f"https://www.topcv.vn/viec-lam-it?page={next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        yield {
            "title": response.xpath('//h1[@class="job-detail__info--title "]//a//text()').get(),
            "salary": response.xpath('//div[@class="job-detail__info--section-content-value"]/text()').get(),
            # "description": response.xpath(".description-selector::text").get(),
            # "company": response.css(".description-selector::text").get(),
            # "location": response.css(".description-selector::text").get(),
            # "requirements": response.css(".description-selector::text").get(),
            # "benefits": response.css(".description-selector::text").get(),
        }
