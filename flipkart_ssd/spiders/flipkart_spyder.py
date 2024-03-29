import scrapy
from scrapy.http import Response
import pandas as pd


class FlipkartSpyderSpider(scrapy.Spider):
    name = "flipkart_spyder"
    allowed_domains = ["flipkart.com"]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
    }

    def start_requests(self):
        for page in range(17):
            url = f"https://www.flipkart.com/search?q=ssd&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}"
            yield scrapy.Request(
                url, callback=self.parse_listPage, headers=self.headers
            )

    # function to get list page

    def parse_listPage(self, response):
        products = response.xpath('.//div[@class="_4ddWXP"]')
        data = list()

        for product in products:
            name = product.xpath('.//a[@class="s1Q9rs"]/text()').get()
            href = "https://www.flipkart.com{}".format(
                product.xpath('.//a[@class="s1Q9rs"]/@href').get()
            )
            price = product.xpath('.//div[@class="_30jeq3"]/text()').get()
            discount = product.xpath('.//div[@class="_3Ay6Sb"]/span/text()').get()

            yield scrapy.Request(
                href,
                callback=self.get_details,
                headers=self.headers,

    # meta is used to send list page extracted data to be called in next get details func
                meta={"name": name, "price": price, "discount": discount},
            )


    # function to get detail page

    def get_details(self, response):
        name = response.meta.get("name")
        price = response.meta.get("price")
        discount = response.meta.get("discount")
        rating = response.xpath(".//div[@class='_3LWZlK']/text()").get()
        offers = response.xpath(".//span[@class='_3j4Zjq row']/li/span/text()").getall()
        capacity = response.xpath(
            ".//a[@class='_1fGeJ5' or @class = '_1fGeJ5 PP89tw']/text()"
        ).getall()
        seller = response.xpath(".//div[@class='_1RLviY']/span/span/text()").get()
        highlight = response.xpath(".//div[@class='_2418kt']/ul/li/text()").getall()
        services = response.xpath(".//div[@class='_2MJMLX']/text()").getall()
        desc = response.xpath(".//div[@class='_1mXcCf RmoJUa']/text()").get()


        yield {
            "Name": name,
            # "Link": response.href,
            "Price": price,
            "Discount": discount,
            "Rating": rating,
            "Offers": offers,
            "Capacity": capacity,
            "Seller Name": seller,
            "Highlights": highlight,
            "Services": services,
            "Description": desc,
        }



#  to run crawler simply execute the line in terminal

# scrapy crawl flipkart_spyder -o filename.csv 


