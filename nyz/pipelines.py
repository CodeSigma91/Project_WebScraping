

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

# class NyzPipeline(object):
# 	def process_item(self, item, spider):
# 		return item

# class ValidateItemPipeline(object):
# 	def process_item(self, item, spider):
# 		if not all(item.values()):
# 			raise DropItem("Missing values!")
# 		else:
# 			return item

class WriteItemPipeline(object):
	def __init__(self):
		self.filename 	= 'nyc_trulia.csv'
	def open_spider(self, spider):
		self.csvfile 	= open(self.filename, mode='wb')
		self.exporter 	= CsvItemExporter(self.csvfile)
		self.exporter.start_exporting()
	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()
	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
		
#, newline='\n'