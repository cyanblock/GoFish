# app.py or run.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def fetch_weather():
    lat = '29.8833'  # Replace with your location's latitude
    lon = '97.9414'  # Replace with your location's longitude
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,windspeed_10m'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current_temp = data['hourly']['temperature_2m']['0']['value']
            current_wind_speed = data['hourly']['windspeed_10m']['0']['value']
            return {'temperature': current_temp, 'windspeed': current_wind_speed}
        else:
            return None
    except requests.exceptions.RequestException:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    categories = request.args.getlist('categories')

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400


    api_key = 'AIzaSyDa83ukRR4dlqykb_5NmxRm3o-BKj6_zkY'
    cx = '674dd5606f7914a34'
    search_parameters = {
        'q': query,
        'key': api_key,
        'cx': cx,
        'siteSearch': '.gov',
        'siteSearch': 'tpwd.texas.gov',
        'siteSearch': 'fisheries.noaa.gov',
        'siteSearch': 'in-fisherman.com',
        'siteSearch': 'nps.gov',  # Restrict search to .gov sites
        #'siteSearch': 'takemefishing.org',
        #'siteSearch': 'saltstrong.com',
        'siteSearchFilter': 'i'   # i: Include results from the specified site(s)
    }

    if categories:
        category_filter = ' OR '.join(categories)
        search_parameters['q'] += f' ({category_filter})'

    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}'

    response = requests.get(url, params=search_parameters)
    data = response.json()

    if 'items' not in data:
        return jsonify({"error": "No results found"}), 404

    return render_template('results.html', results=data['items'])

if __name__ == '__main__':
    app.run(debug=True)
