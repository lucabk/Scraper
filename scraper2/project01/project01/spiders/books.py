import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BookItem    
from scrapy.loader import ItemLoader

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
        # create an ItemLoader instance for the BookItem class populated with response from the parser
        l = ItemLoader(item=BookItem(), response=response) 
        l.add_css("title", "h1")
        l.add_css("price", "p.price_color")
        
        return l.load_item()
