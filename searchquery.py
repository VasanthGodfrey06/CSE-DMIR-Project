import os
from query import advanced_search,get_unique_values
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

client = Elasticsearch(hosts=["http://localhost"], http_auth=("elastic", os.getenv('ELASTICSEARCH_PASSWORD')), port=os.getenv('ELASTCSEARCH_PORT'))

INDEX = os.getenv('ELASTICSEARCH_INDEX')

def search(query, year, movie, composer, lyricist, singer, checkbox):
    query_body_1 = advanced_search(query, year, movie, composer, lyricist, singer, checkbox)
    print(query_body_1)
    print('Making Advance Search ')
    res = client.search(index=INDEX, body=query_body_1, pretty=True, size = 100)
    return res

def getUniqueDetails():
    query_body_2 = get_unique_values()
    print('Get Details Invoked')
    res = client.search(index=INDEX, body=query_body_2)
    return res
