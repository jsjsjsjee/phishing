from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import re

app = Flask(__name__)
# Enable CORS with origin restrictions
CORS(app, resources={r"/*": {"origins": ["https://phishguardai.web.app", "http://localhost:5173"]}})

# Load the trained model
try:
    model = joblib.load('phishing_model.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
    model = None

# Feature Extraction Function (Must match the one used during training)
def extract_features(url):
    features = []
    
    # 1. Length of URL
    features.append(len(url))
    
    # 2. Number of dots (often multiple subdomains in phishing)
    features.append(url.count('.'))
    
    # 3. Presence of IP address in URL
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    features.append(1 if re.search(ip_pattern, url) else 0)
    
    # 4. Count of sensitive words (often used in phishing)
    sensitive_words = ['login', 'signin', 'bank', 'account', 'update', 'verify', 'secure', 'confirm']
    features.append(sum(1 for word in sensitive_words if word in url.lower()))
    
    # 5. Count of special characters (often used to obfuscate)
    special_chars = ['@', '//', '-', '_', '=', '?', '&']
    features.append(sum(url.count(char) for char in special_chars))
    
    # 6. Has 'https' (1 if yes, 0 if no - many phishing sites use http or free ssl)
    features.append(1 if 'https' in url.lower() else 0)
    
    return features

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Extract features
    features = extract_features(url)
    
    # Predict
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1] # Probability of being phishing (class 1)

    result = "Phishing" if prediction == 1 else "Legitimate"
    
    return jsonify({
        'url': url,
        'result': result,
        'probability': float(probability),
        'safe': bool(prediction == 0)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
