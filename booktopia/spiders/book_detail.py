import scrapy
import pandas as pd
from datetime import datetime
from booktopia.items import BooktopiaItem

class BookDetailSpider(scrapy.Spider):
    name = "book_detail"
    allowed_domains = ["www.booktopia.com.au"]

    def start_requests(self):
        # Read data from the CSV with resolved URLs
        data = pd.read_csv(r"F:\booktopia\booktopia\resolved_urls.csv")
        for index, row in data.iterrows():
            isbn = row['ISBN13']
            url = row['ResolvedURL']

            if pd.notna(url):
                yield scrapy.Request(url=url, 
                                     callback=self.parse_book_details,
                                     meta={'isbn': isbn},                    
                                     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    })

    def parse_book_details(self, response):
        
        isbn = response.meta['isbn']
        item = BooktopiaItem()
        item['ISBN_10'] = isbn
        
        title1 = response.xpath('//*[@class="MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk"]/text()').get('').strip()
        title2 = response.xpath('//*[@class="MuiTypography-root MuiTypography-h3 mui-style-1nbf2lb"]/text()').get('').strip()
        item['title_of_book'] = title1 + ' ' + title2
        
        authors = response.xpath('//div[@class="MuiBox-root mui-style-1ebnygn"]/p/a/span/text()').getall()
        item['author'] = ','.join(authors).strip()
        
        book_data = response.xpath('//div[@class="MuiBox-root mui-style-1ebnygn"]/p[2]/text()').get('').strip()
        parts = book_data.split('|')
        parts = [part.strip() for part in parts]
        format_type = ''
        publication_date = ''
        if len(parts) >= 2:
            format_type = parts[0]
            publication_date = parts[1]

        item['book_type'] = format_type
        if publication_date:
            try:
                item['published_date'] = datetime.strptime(publication_date, "%d %B %Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Error: Unable to parse publication date for ISBN {isbn}: {publication_date}")
        else:
            print(f"Error: Publication date is empty for ISBN {isbn}")
        original_price = response.xpath('//div[@class="MuiStack-root mui-style-cfla3"]/div/div/p/span/text()').get('').strip()
        discounted_price = response.xpath('//div[@class="MuiStack-root mui-style-cfla3"]/div/p/text()').get('').strip()
        
        if original_price == '':
            item['original_price'] = discounted_price
            item['discounted_price'] = ''
        else:
            item['original_price'] = original_price
            item['discounted_price'] = discounted_price          
            
        item['publisher'] = response.xpath('//div[@class="MuiTabs-scroller MuiTabs-hideScrollbar MuiTabs-scrollableX mui-style-12qnib"]/div/div/text()[1]').get('').strip()
        
        no_of_pages_text = response.xpath('//div[@class="MuiTabs-scroller MuiTabs-hideScrollbar MuiTabs-scrollableX mui-style-12qnib"]/div/div/text()[2]').get('').strip()

        if 'Pages' in no_of_pages_text :

            no_of_pages = int(no_of_pages_text.replace('Pages', '').strip())
            item['no_of_pages'] = no_of_pages

        else:
            item['no_of_pages'] = None
        
        yield item


# from scrapy.cmdline import execute
# execute("scrapy crawl book_detail".split(" "))


    
        
