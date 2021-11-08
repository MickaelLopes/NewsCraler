# NEWS CRAWLER 

Crawler that scrape news data from Sydney Morning Herarld and Guardian news paper for a given person.
The Crawler take as entry  the first and last name of person searched. 

## Usage 

Search can be called using cmd line. For example, for searching news on __Elon Musk

``` bash 
python main.py --first Elon --last Musk
```

## Prerequisites

### Libraries 

Install all required libraries in requirements file
```bash
pip install -r requirements.txt 
```

### Guardian API key 

An API key is required to crawl the Guardian. It is possible to subscribe for a free API key on https://open-platform.theguardian.com/.  

Once the API key received, entered the API key into the file : 
```
newsSpider/login.json 
```
