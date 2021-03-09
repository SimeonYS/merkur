import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import MerkurItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class MerkurSpider(scrapy.Spider):
	name = 'merkur'
	start_urls = ['https://merkur.dk/privat/nyheder/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="column is-one-quarter is-card"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="pretitle is-uppercase has-text-black-ter has-text-centered"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//p[@class="subtitle has-text-centered"]//text()').getall() + response.xpath('//div[@class="content o-richtext"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=MerkurItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
