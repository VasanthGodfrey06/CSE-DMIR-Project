# Elastic Search Engine

Building Text Corpus and Search Application

# TamilSongsLyricsCorpus

A corpus of lyrics of Tamil Love Songs Lyrics. Original data was scraped from the [website](https://www.tamilbeatslyrics.com/category/tamil-music-directors/a-r-rahman). The repository contains 111 songs lyrics from multiple movies.

The reason to choose the website

- Huge collection of data
- Expected fields present
- Especially, huge data with lyrics in Tamil

# Directory Structure

# Data JSON Structure

##### Every Modified data JSON file has fields of

1. "படம்"
2. "பாடல்"
3. "பாடலாசிரியர்"
4. "இசையமைப்பாளர்"
5. "பாடகர்கள்"
6. "வருடம்"
7. "பாடல்வரிகள்"
8. "உருவகம்"
9. "உவமானம்"
10. "உவமேயம்"

# Setup

- Install ElasticSearch on Your local Machne
- Run ElasticSearch on local by `elasticsearch` on command line
- Run `pip install requirements.txt`
- Run the [bulkdata.py](bulkdata.py) to Create the index and Add Data to Elastic cluster
- Run the [app.py](app.py) to deploy the application
- Go to [http://localhost:5000/search](http://localhost:5000)
- Type some queries and search

# Sample Queries

-
