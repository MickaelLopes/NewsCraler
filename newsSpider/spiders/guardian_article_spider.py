import scrapy
import json
from newsSpider.items import Guardian_Article
from newsSpider.guardian_constants import * 
import newsSpider.secrets as secret
from scrapy.loader import ItemLoader
from  urllib.parse import urlencode
import sys

class GuardianSpider(scrapy.Spider):
    name = "guardian_article"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'newsSpider.pipelines.GuardianSpiderPipeline': 400,
            'newsSpider.pipelines.NewsSpiderPipeline': 500
        }
    }

    def __init__(self, person_name='Mickael', *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)
        self.person_name = person_name

    def start_requests(self):
        self.logger.info(f'Starting crawling for crawler guardian article')

        # Define search variables
        search_variables = GUARDIAN_BASE_SEARCH_VARIABLES
        search_variables['query'] = self.person_name
        
        # Login API key 
        login_file = 'login.json'
        try:
            search_variables['api-key'] = json(open(login_file))["GUARDIAN"]["API_KEY"]
            
        except Exception as e: 
            self.logger.error("Cannot load API KEY for Guardian article spider")
            self.logger.error(f"{e}")
            self.logger.error("Stopping Crawler for Guardian article spider")
            sys.exit(1)

        # Define API URL 

        search_url = GUARDIAN_ROOT_SEARCH_URL + urlencode(search_variables)

        return [scrapy.Request( url=search_url, 
                                callback=self.parse, 
                                errback= self._log_response_error, 
                                cb_kwargs = {'search_variables': search_variables})]

    def parse(self, response, search_variables):
        self.logger.info("parse function initiated")
        self.logger.info(f'Response successful on guardian search for : {self.person_name}')
        
        json_response = json.loads(response.text)
        for result in json_response['response']['results']:
            if result['type'] == 'article': 

                loader = ItemLoader(item=Guardian_Article())

                try: 

                    # Load value in item 
                    loader.add_value('title', result['webTitle'])
                    loader.add_value('article', result['blocks']['body'][0]['bodyTextSummary'])
                    loader.add_value('url',  result['webUrl'])
                    loader.add_value('last_update', result['blocks']['body'][0]['lastModifiedDate'])

                    yield loader.load_item()

                except Exception as e :
                    self.logger.error('Failed to extract data from response')
                    self.logger.error(repr(e))
            
            else : 
                pass
        
        # Crawl next page
        if  (json_response['response']['currentPage'] < json_response['response']['pages']) and json_response['response']['currentPage'] < 3 :
            self.logger.info("Crawling next page")
            
            search_variables['page'] = json_response['response']['currentPage'] + 1

            self.logger.info(f"Starting crawling for page {search_variables['page']}")
            
            search_url = GUARDIAN_ROOT_SEARCH_URL + urlencode(search_variables)

            request = scrapy.Request( url=search_url, 
                                    callback=self.parse, 
                                    errback= self._log_response_error, 
                                    cb_kwargs = {'search_variables': search_variables})

            yield request
    
    def _log_response_error(self,failure): 

        # Log error of spider requests

        self.logger.error(f'Response failed on guardian API for url: {failure.request.url}')
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
