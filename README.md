
# Project_WebScraping

## A Brief Look at NYC Real Estate - A Python Web Scraping Project

_*This is a web scraping project that focused on completed residential real estate sales (over 13,000) in New York City, as listed on the Trulia website (from May 2018 - January 2019). The website was scraped using a Python Scrapy library.*_

The file structure in this repository is the same as that of an initialized scrapy project. However, I have two spiders in this project.

The first one, nyz_spider was built to parse individual listing pages for information. After scraping for a brief period of time, the spider was rejected by the trulia.com website. I believe this can be averted with the use of a VPN.

Regardless, in the interest of this project, I created another spider: nyz_lite_spider that instead parses the result pages only for information. This was more successful, producing over 13,000 observations. However, this method meant abandoning the Property Type and Age features that I originally intended on using for analysis.