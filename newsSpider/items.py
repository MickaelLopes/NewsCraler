# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from html2text import html2text
from itemloaders.processors import MapCompose , TakeFirst

class SMH_Article(Item):
    # define the fields forc your item here like:
    source = Field(output_processor = TakeFirst())
    url = Field(output_processor = TakeFirst())
    title = Field(output_processor = TakeFirst())
    article = Field(
        input_processor = MapCompose(html2text),
        output_processor = TakeFirst()
    )
    last_update = Field(output_processor = TakeFirst())


class Guardian_Article(Item):
    # define the fields for your item here like:
    source = Field(output_processor = TakeFirst())
    url = Field(output_processor = TakeFirst())
    title = Field(output_processor = TakeFirst())
    article = Field(output_processor = TakeFirst())
    last_update = Field(output_processor = TakeFirst())