# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import psycopg2

prevLinks = []
nextLinks = []

class VisonspiderSpider(scrapy.Spider):
    name = 'visonSpider'
    start_urls = ['https://www.wikipedia.org/']

    def parse(self, response):
        # Cursor for the db
        
        try:
            conn = psycopg2.connect(
                host = "127.0.0.1",
                database = "vison",
                user = "postgres",
                password = "9681"
            )
            

            cur = conn.cursor()
            
            # Set default meta information for first page
            from_url = ''
            from_text = ''
            depth = 0
            # Extract the meta information from the response, if any
            if 'from' in response.meta:
                from_url = response.meta['from']
            if 'text' in response.meta:
                from_text = response.meta['text']
            if 'depth' in response.meta:
                depth = response.meta['depth']

            # Update the print logic to show what page contain a link to the
            # current page, and what was the text of the link
            self.start_urls.append(response.url)
            print(depth, response.url, '<-', from_url, from_text, sep=' ')
            
            cur.execute("INSERT INTO urls VALUES (%s,%s);", (response.url,1))
            
            conn.commit()
            conn.close()

        except(Exception, psycopg2.DatabaseError) as error :
            print("Error while interfacing with PostgreSQL table", error)

        page = response.url.split("/")[-2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

        a_selectors = response.xpath("//a")
        for selector in a_selectors:
            text = selector.xpath("text()").extract_first()
            
            global prevLinks, nextLinks
            
            nextLinks = selector.xpath("@href").getall()

            if len(prevLinks) == 0:
                prevLinks = nextLinks.copy()
                link = nextLinks[0]
                request = response.follow(link, callback=self.parse)
            else:

                if response.url in nextLinks:
                    nextLinks.remove(response.url)
                    print("Already Visited....")
                
                else:
                    # Removing urls which are present in both previous and upcomming urls
                    intersection = list(set(prevLinks) & set(nextLinks))
                    nextLinks = [ele for ele in nextLinks if ele not in intersection]
                    prevLinks = nextLinks.copy()

            if len(nextLinks) == 0:
                link = None #No need to follow empty links
            else:
                link = nextLinks[0]
                request = response.follow(link, callback=self.parse)

                # request = response.follow(link, callback=self.parse)
                # Meta information: URL of the current page
                request.meta['from'] = response.url
                # Meta information: text of the link
                request.meta['text'] = text
                # Meta information: depth of the link
                request.meta['depth'] = depth + 1
                yield request
