from pathlib import Path
import os

from Types import CountryName, EventTopic


### remove duplicates in a list.
### Note: this function does not keep the order of elements in returned list
def removeDuplicate(mylist: list) -> list:
    return list(set(mylist))


### Return the absolute path of the file containing all links from a given topic name and a country
def getAllLinksFilePath(file: str, eventTopic: EventTopic, countryName: CountryName) -> Path:
    return __getFilePath(file, "LinksList", eventTopic, countryName)


### Return the absolute path of the file containing all links from a given topic name and a country
def getParsedResultsFilePath(file: str, eventTopic: EventTopic, countryName: CountryName) -> Path:
    return __getFilePath(file, "ParsedResults", eventTopic, countryName)


### private helper function to reduce code duplication
def __getFilePath(file: str, fileType: str, eventTopic: EventTopic, countryName: CountryName) -> Path:
    dataFolderPath: Path = __changeToDataFolder(file)
    outputFileName = dataFolderPath.joinpath(fileType + "_" + countryName.name.replace(" ", "") + "_" + eventTopic.topicName.capitalize() + ".csv")
    return Path(outputFileName)


### Returns the "rootFolder/data" Path where [file] is the path of "rootFolder/[code folder]/file.py"
def __changeToDataFolder(file: str) -> Path:
    currentDirectory = Path(os.path.abspath(__file__)).parents[1]
    dataFolderPath: Path = Path(currentDirectory / 'data' )
    return dataFolderPath