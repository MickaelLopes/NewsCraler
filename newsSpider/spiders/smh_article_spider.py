from types import resolve_bases
import scrapy
import json
from newsSpider.items import SMH_Article
from scrapy.loader import ItemLoader
from newsSpider.smh_constants import *
from urllib.parse import urlencode


from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


class SMHSpider(scrapy.Spider):
    name = "smh_article"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'newsSpider.pipelines.SMHSpiderPipeline': 400,
            'newsSpider.pipelines.NewsSpiderPipeline': 500
        }
    }
    def __init__(self, person_name='Mickael', *args, **kwargs):
        super(SMHSpider, self).__init__(*args, **kwargs)
        self.person_name = person_name

    def start_requests(self):
        
        # Define search variables 
        search_variables = SMH_BASE_SEARCH_VARIABLES
        search_variables['query'] = self.person_name
        
        return [scrapy.http.JsonRequest(    url=SMH_ROOT_SEARCH_URL, 
                                            callback=self.parse_search, 
                                            data = {'query': SMH_SEARCH_QUERY, 'variables':search_variables }, 
                                            cb_kwargs = {'search_variables': search_variables})]

    def parse_search(self, response,search_variables):
        self.logger.info("parse_search function started")
        
        # Load answer
        json_response = json.loads(response.text)

        for asset in json_response['data']['assetsConnection']['assets']: 
            article_id = asset['id']
            yield response.follow(  url = SMH_ROOT_ARTICLE_CONTENT_URL+article_id, 
                                    callback = self.parse_article,
                                    errback = self._log_response_error,
                                    cb_kwargs = {'article_id': article_id})
        
        # Crawl next page if exists - Inserted counter for now to avoid full crawl
        if (json_response['data']['assetsConnection']['pageInfo']['hasNextPage']== True) and (json_response['data']['assetsConnection']['pageInfo']['endOffset'] < 40): 
            self.logger.info('request for more article')
            search_variables['offset'] = json_response['data']['assetsConnection']['pageInfo']['endOffset'] + 1 
            request =  scrapy.http.JsonRequest(     url=SMH_ROOT_SEARCH_URL, 
                                                    callback=self.parse_search, 
                                                    data = {'query': SMH_SEARCH_QUERY, 'variables':search_variables },
                                                    cb_kwargs = {'search_variables': search_variables})
        
            yield request
    
    def parse_article(self, response, article_id):
        self.logger.info("parse_article function initiated")
        self.logger.info(f'Response successful on article URL for article id : {article_id}')

        
        # Load answer
        json_response = json.loads(response.text)
        loader = ItemLoader(item=SMH_Article())

        try: 
            # Load value in item 
            loader.add_value('title', json_response['asset']['headlines']['headline'])
            loader.add_value('article', json_response['asset']['body'])
            loader.add_value('url',  json_response['urls']['published']['smh']['path'])
            loader.add_value('last_update', json_response['dates']['modified'])

            yield loader.load_item()

        except Exception as e :
            self.logger.error('Failed to extract data from response')
            self.logger.error(repr(e))

    def _log_response_error(self, failure):
        # Log error of spider requests

        self.logger.error(f'Response failed on article URL for article id : {failure.request.cb_kwargs["article_id"]}')
        self.logger.error(repr(failure))
                
        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)