
####################################################################################################

from scrapy import Spider, Request
from nyz.items import nyzItem
import re

####################################################################################################

class nyzliteSpider(Spider):
	name 			= "nyz_lite_spider"
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
		print(result_urls[:2])
		# Request to yield each results page for next level parsing:
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page_listing)

####################################################################################################

	# def parse_result_page(self, response):
	# 	# List of urls to individual page for each separate listing.
	# 	# Step = 3 slicing, since there are 3 identical href attributes in 3 <a> tags:
	# 	indv_listing_page_url 	= response.xpath("//div[@class = 'card  boxBasic backgroundBasic']//a/@href").extract()[::3]
	# 	# Request to yield each individual listing page for next level parsing:
	# 	for url in indv_listing_page_url:
	# 		yield Request(url= 'https://www.trulia.com'+url, callback=self.parse_listing_page)

####################################################################################################

	def parse_result_page_listing(self, response):
		# extracting features(variables) of the listing using unique x.paths (and indexing & subscripting):
		page_listings = response.xpath('//li[@class="xsCol12Landscape smlCol12 lrgCol8"]')
		for listing in page_listings:
			soldPrice		= listing.xpath(".//span[@class='cardPrice h5 man pan typeEmphasize noWrap typeTruncate']/text()").extract()
			soldDate 		= listing.xpath(".//div[@class = 'cardFooter soldFooter typeWeightNormal typeLowlight cardFooter man ptn phm']/a/text()").extract()[1::2]
			
			sqft_list		= listing.xpath(".//ul[@data-testid='cardDescription']//li").extract()		#list of <li> tags
			sqft_values		= listing.xpath(".//ul[@data-testid='cardDescription']//text()").extract() 	# cannot take NA for missing values
			sqft 			= [0] * len(sqft_list)
			j=0	
			for i in range(len(sqft_list)):
				temp 		= sqft_values[j]
				if 'class="iconBed typeReversed"' in sqft_list[i]:
					sqft[i]	= ""
				else:
					sqft[i] = temp
					j 		+= 1
			address			= listing.xpath(".//span[@itemprop='streetAddress']/text()").extract()
			city			= listing.xpath(".//span[@itemprop='addressLocality']/text()").extract()[1::3]
			zipCode			= listing.xpath(".//span[@itemprop='postalCode']/text()").extract()
			
			# Appending spider object(acts like dictionary) with features per listing (populating columns for each row/listing):
			listing 					= nyzItem()
			listing['soldPrice'] 		= soldPrice
			listing['soldDate'] 		= soldDate
			listing['sqft'] 			= sqft
			listing['address'] 			= address
			listing['city'] 			= city
			listing['zipCode'] 			= zipCode
			
			yield listing

####################################################################################################
# <li class="iconBed typeReversed"></li>
# <span itemprop="addressLocality" data-reactid="264">
####################################################################################################