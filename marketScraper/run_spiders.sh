#!/bin/bash

#call the spiders 
scrapy crawl dataJumbo
scrapy crawl dataCoto
#run the scrip to post process data obtained
python marketScraper/postProcessing.py








