import scrapy
import json

class targetspider(scrapy.Spider):
    name = "target"

    def start_requests(self):
        #origianl product url: https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab
        #this webpage is dynamic, it loads product details dymanically at renderring time from an API, following the next url structure:
        #https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=84616123&store_id=2184&pricing_store_id=2184
        #so we use this API to get scrape products details, check the readme file for more details!
        url = 'https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab'
        api_url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=84616123&store_id=2184&pricing_store_id=2184'
        self.headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "referer": "https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109" 
            }
        #passing original product url in the meta of this request
        yield scrapy.Request(api_url, headers=self.headers, callback=self.parse, meta = {'original_url':url})
    
    def parse(self, response,):
        #converting request response to a json object
        json_response = response.json()
        #parsing list of products variations
        variations = json_response['data']['product']['children']
        print (f'there are {len(variations)} variations of this product')
        products_list = []
        #parsing product details for each variations
        for var in variations:
            product_details = {}
            product_details['description'] = var['item']['product_description']['downstream_description']
            product_details['specifications'] = var['item']['product_description']['bullet_descriptions']
            product_details['highlights'] = var['item']['product_description']['soft_bullets']['bullets']
            product_details['images_urls'] = [json_response['data']['product']['item']['enrichment']['images']['primary_image_url']] + json_response['data']['product']['item']['enrichment']['images']['alternate_image_urls']
            product_details['title'] = var['item']['product_description']['title']
            product_details['current_retail'] = var['connected_commerce']['products'][0]['locations'][0]['carriers'][0]['price']['current_retail']
            product_details['installment'] = var['connected_commerce']['products'][0]['locations'][0]['carriers'][0]['price']['payment_plan']['installment']
            products_list.append(product_details)
        
        #quesions and answers are not existed on this API response, target.com uses another API for this info
        #Q&A API url for this product, with size parameter adjusted to 100 to show all question on 1 page only
        questions_api_url = 'https://r2d2.target.com/ggc/Q&A/v1/question-answer?type=product&questionedId=84616123&page=0&size=100&sortBy=MOST_ANSWERS&key=c6b68aaef0eac4df4931aae70500b7056531cb37&errorTag=drax_domain_questions_api_error'
        #passing parsed data in the meta of this new request
        yield scrapy.Request(questions_api_url, headers=self.headers, callback=self.parse_qa, meta = {'original_url':response.meta['original_url'],'products_list':products_list})

    def parse_qa(self, response,):
        #converting request response to a json object
        json_response = response.json()
        questions_answers_list = []
        for r in json_response['results']:
            question = {}
            question['question'] = r['text']
            question['answer'] = [x['text'] for x in r['answers']]
            questions_answers_list.append(question)
        print ('Showing products details for the next URL:')
        print(json.dumps(response.meta['original_url'], indent=4, sort_keys=True))
        print ("here's a list of products details for each variation for this product:")
        print(json.dumps(response.meta['products_list'], indent=4, sort_keys=True))
        print ("here's a list of questions and answers for this product:")
        print(json.dumps(questions_answers_list, indent=4, sort_keys=True))
        print ('Thanks')

        