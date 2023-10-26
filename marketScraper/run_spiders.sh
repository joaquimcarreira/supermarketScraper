#!/bin/bash
#change the env
source /home/joaquim/miniconda3/bin/activate market_scraper
#call the spiders 
scrapy crawl dataJumbo
scrapy crawl dataCoto
#run the scrip to post process data obtained
python marketScraper/postProcessing.py








