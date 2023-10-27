# marketScraper
Dada la inflacion actual en Argnetina, me senti motivado en construir una herramienta que permita tener acceso rapido y facil a los precios de los productos en distintos supermercados. 

Esta aplicacion scrapea el ecommerce de los supermercados Coto y Jumbo, obteniendo el nombre del producto, su precio y a que categoria corresponde. Tambien se le adiere la fecha de obtencion para tener un registro historico de precios.
Para contruirla, utilice Python y la libreria Scrapy, que me permite tener un entorno ordenado para futuras ampliaciones de la aplicacion. El metodo de obtencion de los datos es distinta para cada supermercado. Para Coto utilice 
principalmente Xpath para encontrar los elementos html de las paginas. En el caso de Jumbo, logre encontrar los links de request para obtener los datos directamente desde el backend, siendo el principal desafio encontrar los ids de los 
productos y la estructura arbolea de los mismos con sus respectivas categorias y sub-categorias.
A su vez, la aplicacion cuenta con un pequeño post procesado que transforma los datos en un formato conveniente para realizar analisis de mercado.

La aplicacion se inicia ejecutando un archivo bash

Aprendi como utilizar xpath y como funciona el backend de los ecommerce. Tambien gane experiencia en el framework scrapy. 
