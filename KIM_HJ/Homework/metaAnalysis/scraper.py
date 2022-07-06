import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "hyunjoon"
    start_urls = [
        "https://pubmed.ncbi.nlm.nih.gov/?term=%28cerebral+palsy+or+CP%29+and+%28repetitive+transcranial+magnetic+stimulation+or+rTMS+or+tDCS+or+transcranial+direct+current+stimulation%29+and+%28motor%29&sort=pubdate&size=200"
    ]
