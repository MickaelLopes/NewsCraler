import scrapy
from datetime import datetime
import logging
from scrapy.crawler import CrawlerProcess
from newsSpider.spiders.guardian_article_spider import GuardianSpider
from newsSpider.spiders.smh_article_spider import SMHSpider
from scrapy.utils.log import configure_logging

if __name__ == '__main__': 

    # Timestamp for the filenames
    timeStamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    process= CrawlerProcess()
    # process = CrawlerProcess(settings={
    #     'LOG_FILE' : f'log/Log_newsSpider_{timeStamp}.txt',
    #     'LOG_ENABLED': True 
    # }) 
    # process.crawl(SMHSpider, person_name='Hans Smith')
    process.crawl(GuardianSpider, person_name='Hans Smith')
    process.start()

    