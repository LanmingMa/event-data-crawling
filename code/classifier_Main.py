import os
from pathlib import Path

from FindLinks import findLinks, __make_soup
from CrawlParsedData import crawlLink
from Types import CountryName, EventTopic

countryList = [CountryName("United States", "united-states")]
topicInfoList = [EventTopic("finance", 2), EventTopic("technology", 2)]

### Step 1: find all links by going over [countryList] and [topicInfoList]
###         and crawl each link
for country in countryList:
    for topic in topicInfoList:
        findLinks(topic, country)
        crawlLink(topic, country)

### Step 2: tokenize the parsed results and stem
