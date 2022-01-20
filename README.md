# Target.com product details scraper using Scrapy Python framewrok

## Description:
    In this demo project I developed a scrapy project that can extract product details from a product url on target.com.
###    Data points needed to be scraped:-
        - price
        - description
        - specifications
        - highlights
        - questions
        - images urls
        - title
###    Input:
        product url (ex:https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab)
    
## Challenge:
    The main challenge here was that product page on target.com is a dynamic page, meaning that source code of this product page has nothing of these data points needed for scraping. target.com product page is loading these data dynamically while renderring the page in the browser. and because Scrapy framework can only access source code of pages, the static content only not the dynamic content loaded by Javascript, scrapy won't be able to parse these data from this product url on target.com domain.

## Requirements:
    Python 3, Scrapy framework

## Solution:
    after inspecting the product url on target.com domain, I managed to determine what API's are being used to obtain these data points. for example, the following API url is used to show most of products details including (title, price, descriptions,..) except Q&A data, for a specific product:
    https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=84616123&store_id=2184&pricing_store_id=2184
    this API url consists of multiple parameters:
        key: API key for authentication
        tcin: product ID
        store_id: store ID to check availability for this products at specific store
        pricing_store_id: to get prices for speific product at specific store
    and this API url is used to show Q&A data for a specific product:
    https://r2d2.target.com/ggc/Q&A/v1/question-answer?type=product&questionedId=84616123&page=0&size=100&sortBy=MOST_ANSWERS key=c6b68aaef0eac4df4931aae70500b7056531cb37
    this API url consists of multiple parameters:
        type: type of item to show questions about
        questionedId: same as product ID
        page: index for page of questions to show
        size: page size of questions
        sortBy: sorting criteria
        key: an API key for authentication

## Implementation:
    So using these API's we can extract all information related to any product on target.com. Also I noticed that some products have variations for multiple reasons, could be size, color, ...so the current code is extracting products details for each variation there.
    for example, this product under this url:
    https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab
    Apple iPhone 13 Pro Max
    there are 8 variations with different size, colors, RAM size,...
    so, the expected output for this version is printing all products details for each of these variations, with the Q&A section for this product.

## Executing:
    use the following command to run the code 
    `scrapy crawl target`
    you will get the results printed to the terminal screen directly.