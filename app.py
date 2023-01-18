from flask import Flask, render_template, request, redirect
from searchquery import search, getUniqueDetails

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def ui_search():
    response=getUniqueDetails()
    years = [ i["key"] for i in response["aggregations"]["year"]["buckets"] ]
    movies = [ i["key"] for i in response["aggregations"]["movie"]["buckets"] ]
    composers = [ i["key"] for i in response["aggregations"]["composer"]["buckets"] ]
    lyricists = [ i["key"] for i in response["aggregations"]["lyricist"]["buckets"] ]
    singers = [ i["key"] for i in response["aggregations"]["singer"]["buckets"] ]
    details = {"years"  : years, "movies": movies, "composers" : composers, "lyricists": lyricists, "singers" : singers}
    
    if request.method == 'POST':
        query = request.form['searchTerm']
        year = request.form['year']
        movie = request.form['movie']
        composer = request.form['composer']
        lyricist = request.form['lyricist']
        singer = request.form['singer']
        checkbox = "off"
        
        if request.form.get('checkbox') == "on" :
            checkbox = request.form['checkbox']
            
        res = search(query,year,movie,composer,lyricist,singer,checkbox)
        hits = res['hits']['hits']
        time = res['took']
        num_results =  res['hits']['total']['value']
        print(num_results)
        
        return render_template('index.html', query=query, details=details, hits=hits, num_results=num_results,time=time)

    else:
        return render_template('index.html', init='True', details=details)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/search')

if __name__ == '__main__':
    app.run(debug=True)
