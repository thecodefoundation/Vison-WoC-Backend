# Vison-WoC-Backend

Repository for Vison Backened for Winter of Code 2019.

## Current Scenario!

There are millions of pages on the web, all ready to present the information on a variety of interesting and amusing topics. The Search Engines are the messengers of the same information at your disposal whenever you need them. Well, if you go by the technical definition as quoted by [Wikipedia](https://en.wikipedia.org/wiki/Web_search_engine):
“A web search engine is a software system that is designed to search for information on the World Wide Web. The search results are generally presented in a line of results often referred to as search engine results pages (SERPs)”

### The working

Every Search Engines use different complex mathematical algorithms for generating Search Results. Different Search Engines perceive different elements of a web page including page title, content, meta description and then come up with their results to rank on.
The 3 main functions of a Search Engine are:

1. Crawling: A crawler is a Search Engine bot or a Search Engine spider that travels all around the web looking out for new pages ready to be indexed.
2. Indexing: Once the Search Engines crawls the web and comes across the new pages, it then indexes or stores the information in its giant database categorically.
3. Providing information: Whenever a user types in his/her query and presses the enter button, the Search Engines would quest its directory of documents/information (that has already been crawled and indexed) and come back with the most relevant and popular results.

### Why Vison?

These search engines help with searching through words or phrases but what if you could search with a picture or a short video clip?? Won't that be cool.

The Code Foundation is going all out with "The Vison" which enables quick search through images, audio and video.

1. Our especially designed crawler program will travel all over the web and download multimedia(images, videos etc) contents on our servers.

2. We will then index based on various techniques to collect, parse and store the data to facilitate fast and accurate information retrival. 

3. As per the search query Vison would look into it's indexed data and as per the ranking of the content throw back the most relevant and popular results.

### There are two major components of VISON's backend:

1. Crawler: A crawler is a Search Engine bot or a Search Engine spider that travels all around the web looking out for new pages ready to be indexed. To use our experimental crawler click [here](https://github.com/thecodefoundation/Vison-WoC-Backend/blob/master/crawler/vison/README.md).

2. Indexer: Once the Search Engines crawls the web and comes across the new pages, it then indexes or stores the information in its giant database categorically. The aim is to extract information(features) from the crawled and downloaded images(tags, description, title of page) and store the same along with image id so that when searched upon(seach algorithm) can produce relevant data. To use our experimental indexer click [here](https://github.com/thecodefoundation/Vison-WoC-Backend/blob/master/indexer/README.md).

### Todo
1. Crawler: <br>
    - [ ] Update sqlite to postgresql: We want to store the data in a psql database instead of a sqlite database.<br>
    - [ ] Avoid repetition of links: If links visited by the crawler are repeated, the crawler can fall into an infinite trap. If a link is already visited then it must be skipped.
    
2. Indexer: <br>
    - [ ] YOLO v3 trained on 80 classes is currently being used to do object detection on each image. The database is storing the `image id` along with the number of objects in each class. This object detection should extend to many more classes. Better and smarter ideas are welcomed. 
    - [ ] Many a times the user write a query describing a scene/image. For example: `cute kitten with hat.`. In this example kitten and hat share a relationship. Thus visual relationship is of key importance here. You can go through [this](https://www.kaggle.com/c/google-ai-open-images-visual-relationship-track) Kaggle Challenge page on Visual Relationship for more insight. 
    - [ ] It's not just images that is to be indexed. Text material like tags and description for the image should be considered too. NLP can be introduced here.
    - [ ] Build image indexing algorithm and search algorithm for easy and quick retrieval of relevant data for the input seach query. 
    
3. Flask Server:
    - [ ] The Vison UI require a flask server to receive search query, image file, video or link. The server then should send relevant search result to the UI. A example flask server can be found in the `indexer` dir. 
    
Happy Searching :D
