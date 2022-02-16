#!/usr/bin/env python
# coding: utf-8

# In[10]:


#pip install scrapy


# In[70]:


from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose, Compose


# In[71]:


class Articulo(Item):
    codigo= Field()
    category = Field()
    city = Field()
    quarter = Field()
    price = Field()
    area2 = Field()
    rooms = Field()
    baths = Field()
    othert = Field()
    otherv = Field()
    


# In[81]:


class MercadoCrawler(CrawlSpider):
    name = "mecadolibre_scrapy"
    custom_settings={
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT' : 100,
        'FEED_EXPORT_ENCODING' : "utf-8"
    }
    download_delay= 1
    start_urls = ["https://listado.mercadolibre.com.co/inmuebles/arriendo/caldas/"]
    allowed_domains= ["listado.mercadolibre.com.co", "inmueble.mercadolibre.com.co",
                      "apartamento.mercadolibre.com.co","casa.mercadolibre.com.co"]
    
    rules = (
        #Productos
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ), follow=True
        ),
        #Detalle
        Rule(
            LinkExtractor(
                allow=r'/MCO-'
            ), follow=True, callback='parse_items'
        ),
    )
    def limpiarCodigo(self, texto):
        nuevoTexto = texto.replace("#", "")
        return nuevoTexto
    def limpiarCategory(self, texto):
        nuevoTexto = texto.replace(' en Arriendo', "")
        return nuevoTexto
    def limpiarPrecio(self, texto):
        nuevoTexto = texto.replace(' pesos', "").replace('ñ', "n").strip()
        return nuevoTexto
    def limpiarCiudad(self, texto):
        nuevoTexto = texto.split(",")
        return nuevoTexto
    def limpiarBarrio(self, texto):
        nuevoTexto = texto.split(",")
        return nuevoTexto
    def limpiarArea(self, texto):
        nuevoTexto= texto.replace(" m² totales", "")
        return nuevoTexto
    def limpiarHabitaciones(self, texto):
        nuevoTexto=texto.replace(" habitaciones", "").replace(" habitación", "")
        return nuevoTexto
    def limpiarBanos(self, texto):
        nuevoTexto=texto.replace(" baños", "").replace(" baño", "")
        return nuevoTexto
    def limpiarOther(self, texto):
        nuevoTexto=texto.replace(" años", "")
        return nuevoTexto
 
    def parse_items(self, response):
        item = ItemLoader(Articulo(),response)
        item.add_xpath('codigo', '//span[@class="ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD"]/text()', MapCompose(self.limpiarCodigo))
        item.add_xpath('category', '//span[@class="ui-pdp-subtitle"]/text()', MapCompose(self.limpiarCategory))
        item.add_xpath('price', '//span[@class="andes-visually-hidden"]/text()', MapCompose(self.limpiarPrecio))
        item.add_xpath('city', '//p[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"]/text()', MapCompose(self.limpiarCiudad), Compose(lambda v: v[-2]))
        item.add_xpath('quarter', '//p[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"]/text()', MapCompose(self.limpiarBarrio), Compose(lambda v: v[-3]))
        item.add_xpath('area2', '//span[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"]/text()', MapCompose(self.limpiarArea), Compose(lambda v: v[0]))
        item.add_xpath('rooms', '//span[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"]/text()', MapCompose(self.limpiarHabitaciones), Compose(lambda v: v[1]))
        item.add_xpath('baths', '//span[@class="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"]/text()', MapCompose(self.limpiarBanos), Compose(lambda v: v[2]))
        item.add_xpath('othert', '//th/text()', Compose(lambda v: v[4:]))
        item.add_xpath('otherv', '//span[@class="andes-table__column--value"]/text()', Compose(lambda v: v[4:]), MapCompose(self.limpiarOther))
        yield item.load_item()


# In[34]:


#Exportar a .py y ejecutar scrapy runspider mercadolibre_scrapy.py -o mercadolibre.csv -t csv en terminal

