
import scrapy


class nyzItem(scrapy.Item):

	soldPrice		= scrapy.Field()
	soldDate		= scrapy.Field()

	# bed			= scrapy.Field()
	# bath			= scrapy.Field()
	sqft			= scrapy.Field()   
	propertyType 	= scrapy.Field()   
	built			= scrapy.Field()

	address			= scrapy.Field()
	city			= scrapy.Field()
	zipCode			= scrapy.Field()
	
	# priorPrice	= scrapy.Field()
	# priorDate		= scrapy.Field()

