from scrapy.loader import ItemLoader
from ..items import *
import chompjs


class Problems(scrapy.Spider):
    name = 'Problems'
    start_urls = ['https://www.aceptaelreto.com/ws/volume']

    def parse(self, response):

        volume = response.xpath('//id/text()')

        if volume:
            for id in volume:
                url_problemas = 'https://www.aceptaelreto.com/ws/volume/{}/problems/?_=1642276528309'.format(id.get())
                yield scrapy.Request(url=url_problemas, callback=self.parse)
        else:
            problems = response.xpath("//problem")
            for problem in problems:
                # Create item for every problem
                loadedProblem = ItemLoader(item=Problem(), response=response)
                # General data from the problem
                loadedProblem.default_input_processor = TakeFirst()
                loadedProblem.default_output_processor = Join()
                loadedProblem.add_xpath('number', problem.xpath('.//num/text()').get())
                titulo = problem.xpath('.//title/text()').get()
                loadedProblem.add_value('title', titulo)
                # Stadistic data from the problem
                loadedProblem.add_xpath('accepteds', problem.xpath('.//ac/text()').get())
                loadedProblem.add_xpath('no_repeated_accepteds', problem.xpath('.//dacu/text()').get())
                loadedProblem.add_xpath('wrong_answer', problem.xpath('.//wa/text()').get())
                loadedProblem.add_xpath('time_limit', problem.xpath('.//tl/text()').get())
                loadedProblem.add_xpath('memory_limit', problem.xpath('.//ml/text()').get())
                loadedProblem.add_xpath('presentation_error', problem.xpath('.//pe/text()').get())
                loadedProblem.add_xpath('shipments', problem.xpath('.//totalSubs/text()').get())
                loadedProblem.add_xpath('attempts', problem.xpath('.//totalUsers/text()').get())
                loadedProblem.add_xpath('other', problem.xpath('.//ol/text()').get())
                loadedProblem.add_xpath('restricted_function', problem.xpath('.//rf/text()').get())
                loadedProblem.add_xpath('run_time_error', problem.xpath('.//rte/text()').get())
                loadedProblem.add_xpath('compilation_error', problem.xpath('.//ce/text()').get())
                loadedProblem.add_xpath('c_shipments', problem.xpath('.//c/text()').get())
                loadedProblem.add_xpath('cpp_shipments', problem.xpath('.//cpp/text()').get())
                loadedProblem.add_xpath('java_shipments', problem.xpath('.//java/text()').get())
                # loadedProblem['category'] = None
                yield loadedProblem.load_item()


# Get Categories
class Categories(scrapy.Spider):
    name = 'Categories'
    start_urls = ['https://www.aceptaelreto.com/problems/categories.php']

    def parse(self, response):
        # Scrap categories the url with all father categories

        javascript = response.css('script::text').get()
        data = chompjs.parse_js_object(javascript)
        # Create a Category object to save the data

        for data in data['subcats']:
            loadedCategory = ItemLoader(item=Category(), response=response)
            index = int(len(data['path']))
            loadedCategory.add_value('id', data['id'])
            loadedCategory.add_value('name', data['name'])

            # If have some path, have a relation
            # The relation its calculated with the last item in the 'path' and his ID
            if index != 0:
                loadedCategory.add_value('related_category', data['path'][int(index) - 1]['id'])
            else:
                loadedCategory.add_value('related_category', None)
            # Call pipelines to manage the object
            yield loadedCategory.load_item()

            if int(data['numOfProblems']) != 0:
                url_problemas_category = 'https://www.aceptaelreto.com/ws/cat/{}/problems?_=16428085447'.format(
                    data['id'])
                yield scrapy.Request(url=url_problemas_category, callback=self.handleProblemsCategory,
                                     meta={'id': data['id']})

            yield response.follow(
                url='https://www.aceptaelreto.com/problems/categories.php/?cat={}'.format(data['id']),
                callback=self.parse)

    def handleProblemsCategory(self, response):
        problems = response.xpath("//problem")
        for problem in problems:
            loadedCategoryProblem = ItemLoader(item=CategoryProblem(), response=response)
            loadedCategoryProblem.add_value('idCategory', response.meta["id"])
            loadedCategoryProblem.add_xpath('idProblem', problem.xpath('.//num/text()').get())
            yield loadedCategoryProblem.load_item()