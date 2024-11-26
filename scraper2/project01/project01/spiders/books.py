import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    rules = ( 
        # Extract links for pages: https://books.toscrape.com/catalogue/page-2.html
        # and follow links from them (since no callback means follow=True by default)
        Rule(LinkExtractor(allow=(r"catalogue/page-\d+\.html",))),
        
        # Extract links for each book: https://books.toscrape.com/catalogue/BOOKNAME/index.html
        # and parse them with the spider's method parse_book:
        Rule(LinkExtractor(allow=(r"catalogue/[^/]+/index\.html",)), callback="parse_book"),
    )

    def parse_book(self, response):
        yield {
            "title" : response.css("h1::text").get(),
            "price" : response.css("p.price_color::text").get()
        }
