#!/usr/bin/env python
# coding: utf-8

"""
This file contains the functon to parse all links contained in a given website.
Created on Thu Jul 11 17:54:48 2019
@author: shree
"""
import os
from pathlib import Path
import urllib
import urllib.request

from bs4 import BeautifulSoup

from Types import CountryName, EventTopic
from Utils import getAllLinksFilePath


# private helper function to parse a [url] and return the page.
def __make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


# finds all eventbrite.com links related to a given event topic in a given country
# and writes to file 
# TODO: to make this works for meetup.com etc. by passing a website link parameter
def findLinks(eventTopic: EventTopic, countryName: CountryName) -> Path:
    # links corresponding to a specific [eventTopic] in a [country] on eventbrite.com
    links = []

    for rank in range(1, eventTopic.totalNumberPages + 1):
        # TODO: adding country info in this print
        print("Finding links in " + eventTopic.topicName.capitalize() + " topic: page " + str(rank) + " of " + str(eventTopic.totalNumberPages))
        soup = __make_soup("https://www.eventbrite.com/d/" + countryName.urlname + "/" + eventTopic.topicName + "/?page=" + str(rank))
        total_container = soup.find("main", {"data-spec":"search-results"})
        for link in total_container.find_all('a', href = True):
            links.append(link.get('href'))
    
    # write parsed event details to ../data/ folder
    outputFileName: Path = getAllLinksFilePath(__file__, eventTopic, countryName)
    print("Writing to: " + str(outputFileName))
    header = eventTopic.topicName.capitalize() + " Events in " + countryName.name + "\n" 
    file = open(os.path.expanduser(outputFileName), "wb") 
    file.write(bytes(header, encoding= "ascii", errors = "ignore")) 
    for link in links: 
        str_link = link + "\n"
        file.write(bytes(str(str_link), encoding= "ascii", errors = "ignore")) 
        
    file.close()
    return outputFileName
