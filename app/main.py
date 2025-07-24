from flask import Flask, jsonify, request, redirect
from .models import url_store, store_lock
from .utils import generate_short_code, is_valid_url
import time

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL in request body'}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL'}), 400
    # Generate unique short code
    for _ in range(5):  # Try up to 5 times to avoid collision
        short_code = generate_short_code()
        with store_lock:
            if short_code not in url_store:
                url_store[short_code] = {
                    'url': long_url,
                    'clicks': 0,
                    'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
                }
                break
    else:
        return jsonify({'error': 'Could not generate unique short code'}), 500
    short_url = request.host_url.rstrip('/') + '/' + short_code
    return jsonify({'short_code': short_code, 'short_url': short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    with store_lock:
        entry = url_store.get(short_code)
        if not entry:
            return jsonify({'error': 'Short code not found'}), 404
        entry['clicks'] += 1
        target_url = entry['url']
    return redirect(target_url, code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats_short_url(short_code):
    with store_lock:
        entry = url_store.get(short_code)
        if not entry:
            return jsonify({'error': 'Short code not found'}), 404
        return jsonify({
            'url': entry['url'],
            'clicks': entry['clicks'],
            'created_at': entry['created_at']
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)