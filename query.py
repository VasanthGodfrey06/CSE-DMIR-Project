import json

def standard_analyzer(query):
    q = {
        "analyzer": "standard",
        "text": query
    }
    return q


def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        # "highlight": {
        #     "fields": {
        #         "பாடல்வரிகள்": {}
        #     },
        #     "pre_tags" : "<i>",
        #     "post_tags" : "</i>"
        # },
        "size": 150
    }
    return q

def get_unique_values():
    q = {
        "size" : 0,
        "aggs" : {
            "year":{
                "terms":{
                    "field" : "வருடம்",
                    "order" : {
                        "_key" : "asc"
                    },
                    "size" : 100
                }
            },
            "movie":{
                "terms":{
                    "field" : "படம்",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            },    
            "composer":{
                "terms":{
                    "field" : "இசையமைப்பாளர்",
                    "order" : {
                        "_key" : "asc"
                    },
                    "size" : 100
                }
            },
            "lyricist":{
                "terms":{
                    "field" : "பாடலாசிரியர்",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            },
            "singer":{
                "terms":{
                    "field" : "பாடகர்கள்",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            }      
        }
    }
    return q

def advanced_search(query, year, movie, composer, lyricist, singer, checkbox):
    should = []
    must = []
    fields = [year, movie, composer, lyricist, singer]
    if checkbox == "off":
        if all(string == "" for string in fields) :
            q = {'query': {'query_string': {'query': query, 'default_operator': 'or',"analyzer": "inflections"}}}
        else:
            should.append({'query_string': {'query': query, 'default_operator': 'or',"analyzer": "inflections"}})
            if year != "":
                should.append({ "match": { "வருடம்": {"query":year,"operator":"and"} } })
            if movie != "":
                should.append({"match": { "படம்": {"query":movie,"operator":"and"} }})
            if composer != "":
                should.append({"match": { "இசையமைப்பாளர்": {"query":composer,"operator":"and"} }})
            if lyricist != "":
                should.append({"match": { "பாடலாசிரியர்": {"query":lyricist,"operator":"and"} }})
            if singer != "":
                should.append({"match": { "பாடகர்கள்": {"query":singer,"operator":"and"} }})       
            q = {
            "query": {            
                "bool": {
                    "should": should,
                    "minimum_should_match":  1  
                },
            }
            } 
    else:
        if all(string == "" for string in fields) :
            q = {'query': {'query_string': {'query': query, 'default_operator': 'and', "analyzer": "inflections"}}}
        else:
            must.append({'query_string': {'query': query, 'default_operator': 'and', "analyzer": "inflections"}})
            if year != "":
                must.append({ "match": { "வருடம்": {"query":year,"operator":"and"} } })
            if movie != "":
                must.append({"match": { "படம்": {"query":movie,"operator":"and"} }})
            if composer != "":
                must.append({"match": { "இசையமைப்பாளர்": {"query":composer,"operator":"and"} }})
            if lyricist != "":
                must.append({"match": { "பாடலாசிரியர்": {"query":lyricist,"operator":"and"} }})
            if singer != "":
                must.append({"match": { "பாடகர்கள்": {"query":singer,"operator":"and"} }})       
            q = {
            "query": {            
                "bool": {
                    "must": must           
                },
            }
            } 
    return q
def search_with_field(query, field):
    q = {
        "query": {
            "match": {
                [field]: query
            }
        }
    }
    return q


def multi_match(query, fields=['title', 'song_lyrics'], operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q


def agg_multi_match_q(query, fields=['title', 'song_lyrics'], operator='or'):
    q = {
        "size": 500,
        "explain": True,
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        },
        "aggs": {
            "Genre Filter": {
                "terms": {
                    "field": "genre.keyword",
                    "size": 10
                }
            },
            "Music Filter": {
                "terms": {
                    "field": "music.keyword",
                    "size": 10
                }
            },
            "Artist Filter": {
                "terms": {
                    "field": "artist.keyword",
                    "size": 10
                }
            },
            "Lyrics Filter": {
                "terms": {
                    "field": "lyrics.keyword",
                    "size": 10
                }
            }
        }
    }

    q = json.dumps(q)
    return q


def agg_q():
    q = {
        "size": 0,
        "aggs": {
            "Category Filter": {
                "terms": {
                    "field": "genre",
                    "size": 10
                }
            }
        }
    }

    return q


def agg_multi_match_and_sort_q(query, fields, operator='or',sort_num=10):
    print(fields)
    print(query)
    print('sort num is ', sort_num)
    q = {
        "size": sort_num,
        "sort": [
            {"views": {"order": "desc"}},
        ],
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        },
        "aggs": {
            "Genre Filter": {
                "terms": {
                    "field": "வகை.keyword",
                    "size": 10
                }
            },
            "Music Filter": {
                "terms": {
                    "field": "இசையமைப்பாளர்.keyword",
                    "size": 10
                }
            },
            "Artist Filter": {
                "terms": {
                    "field": "பாடியவர்கள்.keyword",
                    "size": 10
                }
            },
            "Lyrics Filter": {
                "terms": {
                    "field": "பாடல் வரிகள்.keyword",
                    "size": 10
                }
            }
        }
    }
    q = json.dumps(q)
    return q