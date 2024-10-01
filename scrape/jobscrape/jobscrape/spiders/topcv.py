import scrapy


class TopcvSpider(scrapy.Spider):
    name = "topcv"
    allowed_domains = ["topcv.vn"]
    start_urls = ["https://www.topcv.vn/viec-lam-it?page=1"]

    def parse(self, response):
        # Extract the items on the page
        items = response.xpath(
            '//div[contains(@class, "job-item-2")]'
        )  # Update this selector
        print(items[1])
        for item in items:
            detail_url = item.xpath(
                "//div[@class='title-block']//a/@href"
            ).get()  # Update this selector
            # print("detail: ", detail_url)
            if detail_url:
                yield response.follow(detail_url, self.parse_item)

        # Handle pagination
        current_page = int(response.url.split("page=")[-1])
        if current_page < 2:
            next_page = current_page + 1
            yield scrapy.Request(
                url=f"https://www.topcv.vn/viec-lam-it?page={next_page}",
                callback=self.parse,
            )

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
