import scrapy
from datetime import datetime
import logging
from scrapy.crawler import CrawlerProcess
from newsSpider.spiders.guardian_article_spider import GuardianSpider
from newsSpider.spiders.smh_article_spider import SMHSpider
from scrapy.utils.log import configure_logging
import sys
import argparse


if __name__ == '__main__': 

    parser = argparse.ArgumentParser(description= "Module to crawl data based on a person name on guardian and sydney morning he")
    parser.add_argument("-f", "--first", required=True, help="First name of the person to search", type=str )
    parser.add_argument("-l","--last", required=True,help = "Last name of the person to search", type=str )
    parser.add_argument("-g", "--guardian", action = 'store_true', help="Only use The Guardian crawler")
    parser.add_argument("-s", "--smh", action='store_true', help="Only use the Sydney Morning Herald crawler")
    args = parser.parse_args()
    
    # Timestamp for the filenames
    timeStamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    process = CrawlerProcess(settings={
        'LOG_FILE' : f'log/Log_newsSpider_{timeStamp}.txt',
        'LOG_ENABLED': True 
    }) 

    if ((args.guardian) & (args.smh)) | ~((args.guardian) & (args.smh)) : 
        process.crawl(SMHSpider, first_name=args.first, last_name=args.last)
        process.crawl(GuardianSpider, first_name=args.first, last_name=args.last)

    elif args.guardian :
        process.crawl(GuardianSpider, first_name=args.first, last_name=args.last)

    elif args.smh : 
        process.crawl(SMHSpider, first_name=args.first, last_name=args.last)
            
    process.start()

    