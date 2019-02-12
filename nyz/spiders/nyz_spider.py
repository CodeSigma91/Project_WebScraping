
####################################################################################################

from scrapy import Spider, Request
from nyz.items import nyzItem
import re

####################################################################################################

class nyzSpider(Spider):
	name 			= "nyz_spider"
	allowed_urls 	= ['https://www.trulia.com/']
	start_urls 		= [
	'https://www.trulia.com/sold/New_York,NY/', 
	'https://www.trulia.com/sold/Brooklyn,NY/', 
	'https://www.trulia.com/sold/Bronx,NY/',
	'https://www.trulia.com/sold/36081_c/',
	'https://www.trulia.com/sold/Staten_Island,NY/']

####################################################################################################
	
	def parse(self, response):
		print(response)
		# Determining number of result pages that distribute the total number of listings:
		of_total_listings 			= response.xpath("//div[@class = 'txtC h6 typeWeightNormal typeLowlight']/text()").extract_first()
		a, results_per_page, total 	= map(lambda x: int(x), re.findall('\d+', of_total_listings))
		number_result_pages 		= (total // results_per_page) + 1
		# list comprehension to generate each result page's url iterated over the number of result pages:
		result_urls 				= [ str(response)[5:-1] + '{}_p/'.format(x) for x in range(1, number_result_pages+1)] #[0:1]# TEST RUN
		print(result_urls[1:10])
		# Request to yield each results page for next level parsing:
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

####################################################################################################

	def parse_result_page(self, response):
		# List of urls to individual page for each separate listing.
		# Step = 3 slicing, since there are 3 identical href attributes in 3 <a> tags:
		indv_listing_page_url 	= response.xpath("//div[@class = 'card  boxBasic backgroundBasic']//a/@href").extract()[::3]
		# Request to yield each individual listing page for next level parsing:
		for url in indv_listing_page_url:
			yield Request(url= 'https://www.trulia.com'+url, callback=self.parse_listing_page)

####################################################################################################

	def parse_listing_page(self, response):
		# extracting features(variables) of the listing using unique x.paths (and indexing & subscripting):
		
		try:
			soldPrice		= response.xpath(".//div[@class = 'mvn']/span/text()").extract_first()[8:-5]
		except TypeError:
			soldPrice		= "te"
			# String is initially in the format: '/n $399,000 /n'. After .strip() its, '$399,000'. Must clean and change type!
		try:
			soldDate 		= response.xpath(".//span[@class = 'typeLowlight typeEmphasize mvn mlm h6']//span/text()").extract()[1][4:]
		except IndexError:
			soldDate 		= "ie"
			# feature put under try/expect since several listings showing as "off market" with no corresponding value(s)
			# Two <span> tags under x.path, tag with 'soldDate' does not have any distinguishing attribute. Output initially, "['Sold', ' on Jan 31, 2019']".
		try:
			sqft			= response.xpath(".//ul[@class = 'listInline man pts ptXxsHidden pbsXxsVisible']/li/text()").extract()[0]
		except IndexError:
			sqft			= "ie"

			# Two <li> tags under x.path, tag with 'sqft' does not have any distinguishing attribute. Output initaill, "['836 sqft', 'Condo']"
		try:
			propertyType	= response.xpath(".//ul[@class = 'listInline man pts ptXxsHidden pbsXxsVisible']/li/text()").extract()[1]
		except IndexError:
			propertyType	= "ie"

			# Used second (index = 1) string in previous x.path list
		try:
			built_check		= response.xpath(".//div[@data-auto-test-id='home-detail']//li/text()").extract()
			# To handle missing 'Year Built' values:
			built 			= list(filter(lambda x: 'Built ' in x, built_check))[0][10:]
		except IndexError:
			built			= "ie"
			# feature put under try/expect in case 'Year built' value is missing. Complete tag text also contains 'property type' and 'sqft'.
		address				= response.xpath(".//div[@data-role = 'address']/text()").extract_first().strip()
			# String is initially in the format: '\n        101 W 24th St #4H\n      '. After .strip() its fine. This is a unique tag
		city				= response.xpath(".//span[@data-role = 'cityState']/text()").extract_first().strip()[:-10]
			# Text under <span> tag in the 'City, State, Zip Code' format: ex. "New York, NY 10011". Removing State & Zip Code for City by indexing. Unique tag.
		zipCode				= response.xpath(".//span[@data-role = 'cityState']/text()").extract_first().strip()[-5:]
			# Using previous x.path and keeping only last five index positions of string for Zip Code.

		# Not available on Trulia (Zillow had it...)
		# priorPrice		=
		# priorDate			= 

		# Appending spider object(acts like dictionary) with features per listing (populating columns for each row/listing):
		listing 					= nyzItem()
		listing['soldPrice'] 		= soldPrice
		listing['soldDate'] 		= soldDate
		listing['sqft'] 			= sqft
		listing['propertyType'] 	= propertyType
		listing['built'] 			= built
		listing['address'] 			= address
		listing['city'] 			= city
		listing['zipCode'] 			= zipCode
		# listing['priorPrice'] 	= priorPrice
		# listing['priorDate'] 		= priorDate

		yield listing

####################################################################################################