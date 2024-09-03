# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

#class WebscraperPipeline:
#    def process_item(self, item, spider):
#        adapter = ItemAdapter(item)
#        
#        # Retrieve and clean the body_text field
#        body_html = adapter.get('body_html', '')
#        cleaned_body_html = ' '.join(body_html.split()).strip()
#        
#        # Update the item with the cleaned text
#        adapter['body_html'] = cleaned_body_html
#        
#        return item

from itemadapter import ItemAdapter
from scrapy.selector import Selector

class WebscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Retrieve the body_html field
        body_html = adapter.get('body_html', '')
        
        # Parse the HTML content using Scrapy's Selector
        selector = Selector(text=body_html)
        
        # Extract text and hyperlinks inline
        body_text = ''
        for element in selector.xpath('//body//*'):
            if element.root.tag == 'a':
                # Process hyperlink if it has related text
                link_text = element.xpath('text()').get()
                link_url = element.xpath('@href').get()
                if link_text and link_url:
                    link_text = link_text.strip()
                    body_text += f"{link_text} ({link_url}) "
            else:
                # Process text content
                text_parts = element.xpath('.//text()').getall()
                if text_parts:
                    text_content = ' '.join(text_parts).strip()
                    body_text += text_content + ' '
        
        # Clean up extra spaces
        cleaned_body_text = ' '.join(body_text.split()).strip()
        
        # Update the item with the cleaned text
        adapter['body_html'] = cleaned_body_text
        
        return item
