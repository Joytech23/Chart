from flask import Flask, request, jsonify, url_for
import requests
import os
from werkzeug.utils import secure_filename
import uuid
app = Flask(__name__)

# Directory to save images
SAVE_DIR = 'static/images'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

@app.route('/')
def home():
    return "Flask app is running!"

# Endpoint to download the image, save it locally, and return the URL
@app.route('/get_chart_image', methods=['GET'])
def get_chart_image():
    try:
        # Get the chart URL from query parameters
        chart_url = request.args.get('chart_url')

        if not chart_url:
            return jsonify({"error": "Chart URL not provided"}), 400

        # Request the image from the chart URL
        response = requests.get(chart_url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch the chart image"}), 400

        # Create a secure filename for the image
        filename = secure_filename(f'chart_image{uuid.uuid4()}.png')

        # Save the image to the static/images directory
        file_path = os.path.join(SAVE_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Generate the URL to the saved image
        image_url = url_for('static', filename=f'images/{filename}', _external=True)

        # Return the image URL as JSON
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
