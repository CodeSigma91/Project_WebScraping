################################################################################
library(dplyr)
library(leaflet)
################################################################################
# setwd()
################################################################################
trulia5 = read.csv('./data/trulia5_complete.csv', stringsAsFactors = FALSE)
trulia5$zipCode = as.factor(trulia5$zipCode)
################################################################################
zipcodeList     = read.csv('./data/ny-zip-code.csv', sep = ';')
zipcodeList$Zip = as.factor(zipcodeList$Zip)
zipcodeList     = zipcodeList %>% rename(zipCode = Zip)
################################################################################
data.city = trulia5 %>%
  select(c(5:9)) %>%
  group_by(zipCode, borough) %>%
  summarize(count=n())
################################################################################
zipcodeList         = zipcodeList %>%
  select(c(1,4,5)) %>% filter(zipCode %in% data.city$zipCode)
data.city           = inner_join(data.city, zipcodeList, by= 'zipCode')
data.city$lat.long  = paste(data.city$Latitude, data.city$Longitude, sep = ':')
data.city$countText = as.character(data.city$count) 
################################################################################
pal =colorNumeric(
  palette = c('Dark Green','Black','Red'),
  domain = data.city$count)
################################################################################
cityMap = leaflet(data = data.city) %>% 
  addTiles() %>% 
  addCircleMarkers(lng    = data.city$Longitude,
                   lat    = data.city$Latitude,
                   radius = 3,
                   label  = data.city$countText,
                   color  = ~pal(count),
                   opacity = 1)
cityMap
################################################################################
