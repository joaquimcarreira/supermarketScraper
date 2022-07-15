#!/bin/bash

source /home/joaquim/miniconda3/bin/activate market_scraper

scrapy crawl preciosCoto

python marketScraper/postProcessing.py








