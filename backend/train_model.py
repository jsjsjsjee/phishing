import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import re

# Feature Extraction Function
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

# Synthetic Dataset Generation
print("Generating synthetic dataset...")
safe_urls = [
    "https://www.google.com", "https://www.youtube.com", "https://www.facebook.com",
    "https://www.amazon.com", "https://www.wikipedia.org", "https://www.yahoo.com",
    "https://www.reddit.com", "https://www.netflix.com", "https://www.instagram.com",
    "https://www.linkedin.com", "https://github.com", "https://stackoverflow.com",
    "https://www.microsoft.com", "https://www.apple.com", "https://twitter.com",
    "https://www.whatsapp.com", "https://www.twitch.tv", "https://weather.com",
    "https://www.nytimes.com", "https://www.cnn.com"
    # Add more synthetic safe variations if needed
]
phishing_urls = [
    "http://secure-login-paypal.com", "http://update-account-bankofamerica.net",
    "http://verify-identity-wellsfargo.org", "http://apple-id-support-team.com",
    "http://192.168.1.1/banking/login.html", "http://google-drive-shared-file.xyz",
    "http://netflix-payment-update-required.net", "http://amazon-order-confirmation.biz",
    "http://facebook-security-check.info", "http://irs-tax-refund-claim.com",
    "http://suspicious-domain-monitor.ru", "http://totally-legit-bank.com/login",
    "http://signin.ebay.com.account-update.tk", "http://mail.google.com.verify.ga"
]

# Create DataFrame
data = []
for url in safe_urls:
    data.append(extract_features(url) + [0]) # 0 for Legitimate

for url in phishing_urls:
    data.append(extract_features(url) + [1]) # 1 for Phishing

columns = ['length', 'dots', 'has_ip', 'sensitive_words', 'special_chars', 'has_https', 'label']
df = pd.DataFrame(data, columns=columns)

# Train/Test Split
X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
print("Training Random Forest Classifier...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluation
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Synthetic Test Set: {accuracy * 100:.2f}%")

# Save Model
model_filename = 'phishing_model.pkl'
joblib.dump(clf, model_filename)
print(f"Model saved to {model_filename}")
