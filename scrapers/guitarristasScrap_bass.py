from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import re
from datetime import datetime, timedelta
import locale


class Instrumento(Item):
    name = Field()
    link = Field()
    price = Field()
    image = Field()
    location = Field() 
    expiration = Field()
    publish = Field()
    category = Field()
    website = Field()


class GuitarristasInfoCrawler(CrawlSpider):
    name = "GuitarristasInfoCrawler"
    allowed_domains = ['guitarristas.info']
    start_urls = ['https://www.guitarristas.info/anuncios/bajos']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 20 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    download_delay = 1

    rules = {
        Rule(LinkExtractor(allow=r'/anuncios/bajos/pagina\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/anuncios/[\w-]+/\d+', restrict_xpaths=['//div[@id="ads"]']), follow=True, callback='parse_items')

    }

    def parse_items(self, response):
        item = ItemLoader(Instrumento(), response)
        item.add_xpath('name', '//h1[@class="title"]/text()')
        item.add_value('link', response.url)
        item.add_xpath('price', '//div[@class="ad-price"]/text()')
        item.add_xpath('image', '//div[@class="full-image"]/a/@href')
        item.add_xpath('location', '//div[@class="layout-simple"]//strong/text()')
        item.add_xpath('expiration', '//div[@class="layout-simple"]//div[@class="expira"]/text()', MapCompose(self.parse_expiration))
        item.add_xpath('category', '//ul[@class="breadcrumb breadcrumb-dark"]/li[3]//span/text()')
        item.add_xpath('publish', '//div[@class="layout-simple"]/div[@class="grid grid-gutter"]/div[@class="col-lg-7"]/div[1]/text()', MapCompose(self.parse_publish))
        item.add_value('website', 'guitarristas.info')
        #itemFinal = item.load_item()
        itemFinal = item.load_item()
        yield itemFinal


    def parse_expiration(self, texto):
        date_str = texto.split('|')[0].replace('Expiración: ', '').strip()
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        return formatted_date
    

    def parse_publish(self, texto):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8' or 'Spanish_Spain')

        textounido = ''.join(texto)
        date_pattern = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')
        match = date_pattern.search(textounido)
        if match:
            # Extract the date string from the matched object
            date_str = match.group(1)
            # Parse the date string into a datetime object if needed
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
            formatted_date = date_obj.strftime('%Y-%m-%d')
            return formatted_date
        
        relative_pattern = re.compile(r'hace (\d+) (semanas|dias)', re.IGNORECASE)
        match = relative_pattern.search(textounido)
        if match:
            amount, unit = match.groups()
            amount = int(amount)
            if 'semana' in unit.lower():
                date_obj = datetime.now().date() - timedelta(weeks=amount)
                formatted_date = date_obj.strftime('%Y-%m-%d')
                return formatted_date 
            elif 'dia' in unit.lower():
                date_obj = datetime.now().date() - timedelta(days=amount)
                formatted_date = date_obj.strftime('%Y-%m-%d')
                return formatted_date

        return None