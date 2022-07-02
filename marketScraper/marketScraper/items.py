from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Compose
import re


def arreglo(x):
    return [x[i]+x[i+1] for i in range(0, len(x)-1, 2)]


def filter_none(x):
    if x:
        return x


def clean_numbers(x):
    return float(re.sub("[^0-9.]", "", x))

def cleanBancos(x):
    dic = {"santander":"Banco Santander",
          "lanacion": "Club La Nacion",
           "logo_nacion":"Banco Nacion",
           "icbc":"Banco ICBC",
           "columbia":"Banco Columbia",
           "patagonia":"Banco Patagonia",
           "hsbc":"Banco HSBC",
           "comafi":"Banco Comafi",
           "rosario":"Banco Municipal",
           "comunidad":"Comunidad Coto",
           "ciudad":"Banco Ciudad",
          "tci":"Tarjeta Coto"}
    for key in dic:
        if key in x:
            x = dic[key]
    return x





class MarketscraperItem(Item):
    date = Field()
    categoria = Field()
    nombres = Field(input_processor=MapCompose(str.strip))
    precios = Field(input_processor=MapCompose(str.strip, filter_none))


class DiscountItem(Item):
    # MapCompose trabja en cada unidad del intirerable, por eso es conveniente usarlo en el input.
    #  Compose trabja sobre todo el itirerable, por eso lo estoy usando en el output
    nombres = Field(input_processor=MapCompose(str.strip))
    precios = Field(input_processor=MapCompose(str.strip, filter_none, clean_numbers),
                    output_processor=Compose(arreglo))
    cantUnidades = Field(input_processor=MapCompose(str.strip))
    porcentaje = Field()
    tipo = Field()


class TreeToUrlJumbo(Item):
    links = Field()

class BancosCoto(Item):
    nombre = Field(input_processor=MapCompose(cleanBancos))
    descuento = Field()
    dia = Field()
    condiciones = Field()