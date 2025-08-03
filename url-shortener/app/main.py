from flask import Flask, jsonify, request, redirect, url_for
from .models import url_store
from .utils import validate_url, create_response, format_url_data

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
        return create_response({"error": "URL is required"}, 400)
    
    url = data['url']
    if not validate_url(url):
        return create_response({"error": "Invalid URL provided"}, 400)
    
    # Create short URL
    mapping = url_store.add_url(url)
    base_url = request.host_url.rstrip('/')
    
    return create_response(format_url_data(base_url, mapping))

@app.route('/<short_code>')
def redirect_to_url(short_code):
    mapping = url_store.get_url(short_code)
    if not mapping:
        return create_response({"error": "URL not found"}, 404)
    
    # Increment click count
    url_store.increment_clicks(short_code)
    return redirect(mapping.original_url)

@app.route('/api/stats/<short_code>')
def get_url_stats(short_code):
    mapping = url_store.get_url(short_code)
    if not mapping:
        return create_response({"error": "URL not found"}, 404)
    
    base_url = request.host_url.rstrip('/')
    return create_response(format_url_data(base_url, mapping))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)