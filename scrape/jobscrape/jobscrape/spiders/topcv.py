import scrapy


class TopcvSpider(scrapy.Spider):
    name = "topcv"
    allowed_domains = ["topcv.vn"]
    start_urls = ["https://www.topcv.vn/viec-lam-it?page=1"]
    page_limit = 20

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
            "company": response.xpath('//h2[@class="company-name-label"]/a/text()').get(),
            "salary": response.xpath('//div[@class="job-detail__info--section-content-value"]/text()')[0].get(),
            "city": response.xpath('//div[@class="job-detail__info--section-content-value"]/text()')[1].get(),
            "experience": response.xpath('//div[@class="job-detail__info--section-content-value"]/text()')[2].get(),
            "description": response.xpath('(//div[@class="job-description__item--content"])[1]//ul//li').getall(),
            "requirement": response.xpath('(//div[@class="job-description__item--content"])[2]//ul//li').getall(),
            "benefit": response.xpath('(//div[@class="job-description__item--content"])[3]//ul//li').getall(),
            "location": response.xpath('(//div[@class="job-description__item--content"])[4]/div/text()').get(),
            "domain": "topcv",
            "link": response.url,
            "deadline": response.xpath('//div[@class="job-detail__information-detail--actions-label"]/text()').get(),
        }
