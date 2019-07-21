#!/usr/bin/env python
# coding: utf-8

"""
This file contains method to parse a given event page at eventbrite.com and save parsed results into a file
Created on Mon Jul 15 07:06:36 2019

@author: shree
"""

import csv
from pathlib import Path
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

from Types import EventTopic, CountryName
from Utils import getAllLinksFilePath, getParsedResultsFilePath, removeDuplicate

# for a given topic 
def crawlLink(eventTopic: EventTopic, countryName: CountryName) -> Path:
    # read all links from file and remove duplicate links
    linksPath: Path = getAllLinksFilePath(__file__, eventTopic, countryName)
    linksFile = open(linksPath, 'r')
    csv_file = csv.reader(linksFile)
    next(csv_file, None)
    linkList = []
    for row in csv_file:
        linkList.append(row[0])
    linkList = removeDuplicate(linkList)

    # create output file
    outputFileName = getParsedResultsFilePath(__file__, eventTopic, countryName)
    outputFile = open(outputFileName, "w", encoding = "utf-8")
    headers = "Event_Name,Organizer,Cost,Date_and_Time,Location,About_Event\n"
    outputFile.write(headers)

    for i in range(0,len(linkList)):
        my_url = linkList[i]
        print("Crawling the " + str(i) + "th link of " + str(len(linkList)) + ": ", my_url)
    
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        # HTML PARSER
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class":"g-cell g-cell-1-1 g-cell-lg-4-12 g-cell--no-gutters listing-hero__detailed-info"})
        
        ## skip empty content
        if not containers:
            continue
        container = containers[0]
    
        # EVENT NAME
        title = container.h1 
        if title:
            event_title = title.text
        else:
            event_title = 'N/A'
    
        # ORGANIZER NAME
        organizer = container.div.a
        if organizer:
            event_organizer = organizer.text.strip()
        else:
            event_organizer = 'N/A'
    
        # COST OF THE EVENT
        cost_containers = container.findAll("div", {"class":"js-display-price"})
        if cost_containers:
            cost_container = cost_containers[0]
            event_cost = cost_container.text.strip()        
        else:
            event_cost = 'N/A'
    
        # Event Details
        ## DATE AND TIME
        date_containers = page_soup.findAll("div", {"class":"event-details__data"})
        if date_containers:
            date_container = date_containers[0]
            dates = date_container.findAll("p",{}) 
            for i in range(len(dates) - 1):
                event_date = event_date + dates[i].text.strip()
        else:
            event_date = "N/A"
        
        ## LOCATION
        if date_containers:
            location_container = date_containers[1]
            location = location_container.p
            location = location_container.findAll("p",{}) 
            for i in range(len(location) - 1):
                event_location = location[i].text.strip() + ' '
        else:
            event_location = "N/A"
        

        #ABOUT THIS EVENT
        #about_containers = page_soup.findAll("div", {"class":"structured-content-rich-text structured-content__module l-align-left l-mar-vert-6 l-sm-mar-vert-4 text-body-medium"})
        #len(about_containers)
        
        # DESCRIPTION OF THE EVENT
        description_containers = page_soup.findAll("div", {"class":"g-cell g-cell-10-12 g-cell-md-1-1"})
        if description_containers:
            event_description = ""
            description_container = description_containers[0]
            description = description_container.findAll("p",{})
            count = len(description)
            for i in range(0,count):
                event_description = event_description + description[i].text.strip()
        else:
            event_description = "N/A"
        
        #TAGS
        #tags_containers = page_soup.find_all
        
        #PRINTING ALL THE GATHERED INFORMATION
        # print("\n\n\n\nEvent Name: " + event_title)
        # print("Organizer: " + event_organizer)
        # print("Cost: " + event_cost)
        # print("Date and Time: " + event_date)
        # print("Location/Address: " + event_location)
        # print("Event Description: " + event_description)    

        # write to file
        outputFile.write(event_title + "," + event_organizer + "," + event_cost + "," + event_date.replace(",","|") + "," + event_location.replace(",","|") +"," + event_description.replace(",","|") + "\n")
        
    outputFile.close()
    return outputFileName
    