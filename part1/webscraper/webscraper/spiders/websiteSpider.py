import scrapy
from webscraper.items import WebscraperItem

class WebsitespiderSpider(scrapy.Spider):
    name = "websiteSpider"
    allowed_domains = ["books.toscrape.com", "seetickets.com"]
    start_urls = [
        "https://books.toscrape.com",
        "https://www.seetickets.com",
    ]
    
    custom_settings = {
        'FEEDS': {
            'data.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response):
        # Create an instance of WebscraperItem
        web_item = WebscraperItem()
        
        # Extract the body content as HTML
        body_html = response.xpath('//body').get()
        
        # Assign the HTML content to the item
        web_item['body_html'] = body_html
        
        # Yield the item to the Scrapy pipeline
        yield web_item
