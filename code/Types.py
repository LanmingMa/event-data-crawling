from dataclasses import dataclass

# each countryName includes a name string and a urlname which is how it's represented in url
@dataclass(frozen = True)
class CountryName:
    name: str
    urlname: str

# each topic item is a pair of a topic name a string and its total number of pages on eventbrite.com
@dataclass(frozen = True)
class EventTopic:
    topicName: str
    totalNumberPages: int