# NEWS CRAWLER 

Crawler that scrape news data from Sydney Morning Herarld and Guardian news paper for a given person.
The Crawler take as entry  the first and last name of person searched. 

## Usage 

Search can be called using cmd line. For example, for searching news on __Elon Musk

``` bash 
python main.py --first Elon --last Musk
```

### Specific Crawler

if you want to use a particular crawler (guardian or SMH), use the following tags -s (for SMH) or -g (for the guardian): 
```bash 
python main.py --first Elon --last Musk -s 
python main.py --first Elon --last Musk -g 
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

## Output file

### logfile
Each time the crawler is run, a timestamp log file is created under the folfer
```
\log\
``` 

### data
The data crawl from the news website are save in timestamp json file under the folder : 
```
\output\
``` 
Each article scraped contains the following fields : 
- title : Headline of the article
- article : body of the article 
- url : URL path of the article
- last_update : last modified date of the article
- source : Source of the article (either _Guardian_ or _SMH_)  