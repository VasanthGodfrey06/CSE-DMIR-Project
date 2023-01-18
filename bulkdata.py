import os
import codecs
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()

client = Elasticsearch(hosts=["http://localhost"], http_auth=("elastic", os.getenv('ELASTICSEARCH_PASSWORD')), port=os.getenv('ELASTICSEARCH_PORT'))
INDEX = os.getenv('ELASTICSEARCH_INDEX')

# Creating index if not manually created
def createIndex():
    # Create an index
    res = client.indices.create(index=INDEX)

    # Read mappings from a JSON file
    with codecs.open('analyzers/mapping_file.json', 'r', encoding="utf-8") as file:
        mappings = json.load(file)

    # Read a setting from a JSON file
    with codecs.open('analyzers/setting.json', 'r', encoding="utf-8") as settings_file:
        settings = settings_file.read()
    
    # Add settings to the index
    client.indices.close(index=INDEX)
    client.indices.put_settings(index=INDEX, body=settings, pretty=True)
    client.indices.open(index=INDEX)

    # Add mappings to the index
    client.indices.put_mapping(index=INDEX, body=mappings, pretty=True)
    
    print(res)

def read_all_songs():
    with open('corpus/Tamil Love Songs Lyrics.json', 'r', encoding='utf-8-sig') as f:
        all_songs = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")
        res_list = [i for n, i in enumerate(all_songs) if i not in all_songs[n + 1:]]

        return res_list

def genData(song_array):
    for song in song_array:
        # Fields-capturing
        title = song.get("பாடல்", None)
        movie = song.get("படம்",None)
        lyricist = song.get("பாடலாசிரியர்", None)
        composer = song.get("இசையமைப்பாளர்", None)
        singers = song.get("பாடகர்கள்", None)
        year = song.get("வருடம்", None)
        lyrics = song.get("பாடல் வரிகள்", None)
        metaphor = song.get("உருவகம்", None)
        source = song.get("உவமானம்", None)
        target = song.get("உவமேயம்", None)

        yield {
            "_index": INDEX,
            "_source": {
                "பாடல்": title,
                "படம்": movie,
                "பாடலாசிரியர்": lyricist,
                "இசையமைப்பாளர்": composer,
                "பாடகர்கள்": singers,
                "வருடம்": year,
                "பாடல் வரிகள்": lyrics,
                "உருவகம்": metaphor,
                "உவமானம்": source,
                "உவமேயம்": target
            },
        }

createIndex()
all_songs = read_all_songs()
helpers.bulk(client, genData(all_songs))