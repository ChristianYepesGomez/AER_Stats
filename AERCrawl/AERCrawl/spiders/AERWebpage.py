from scrapy.loader import ItemLoader
from ..items import *

class Problems(scrapy.Spider):
    name = 'Problems'
    id_problem = 100
    start_urls = ['https://www.aceptaelreto.com/problem/statement.php?id={}'.format(id_problem)]

    def parse(self, response):

        if(response.xpath('/html/body/div[1]/div/div[2]/strong/text()').get() != "ERROR: "):
            loadedProblem = ItemLoader(item=Problem(), response=response)
            loadedProblem.add_xpath('title', '/html/body/div[1]/div/div[2]/div/div[2]/h1/text()')
            yield loadedProblem.load_item()
            Problems.id_problem = Problems.id_problem + 1
            next_page = 'https://www.aceptaelreto.com/problem/statement.php?id={}'.format(Problems.id_problem)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            pass
