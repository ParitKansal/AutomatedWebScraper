import scrapy
from webscraper.items import WebscraperItem

class WebsitespiderSpider(scrapy.Spider):
    name = "websiteSpider"
    allowed_domains = ["www.amazon.in"]
    start_urls = [
        "https://www.amazon.in/Nike-Mens-White-Black-White-Sneakers/dp/B098F462JJ/ref=sr_1_6?psc=1",
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
        
        # Assign the HTML content and URL to the item
        web_item['url'] = response.url
        web_item['body_html'] = body_html
        
        # Yield the item to the Scrapy pipeline
        yield web_item
        
        """
        # Extract and follow links to other pages on the website
        for href in response.xpath('//a/@href').extract():
            # Build the absolute URL
            url = response.urljoin(href)
            # Check if the URL has a valid scheme
            if url.startswith(('http://', 'https://')):
                # Follow the link
                yield scrapy.Request(url, callback=self.parse)
        """
