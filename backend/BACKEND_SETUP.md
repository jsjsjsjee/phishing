# Backend Setup Guide

This guide explains how to run the backend for the PhishGuard AI project and how to connect it to the frontend.

## Local Development

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Navigate to the `backend` folder and install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Backend
Start the Flask server:
```bash
python app.py
```
The backend will run on `http://localhost:5000`.

## Connecting to Frontend

The frontend uses environment variables to find the backend. By default, it looks for `http://localhost:5000`.

If you change the backend port or deploy it to a different address, update your `.env` files in the `frontend` directory:

```env
VITE_API_URL=https://your-backend-url.com
```

## Deployment Options

Since the frontend is hosted on Firebase Hosting (which hosts static files), you need to host the Python backend separately on a service that supports Flask/Python.

### Suggested Platforms:
1. **Render** (Easy to use, free tier available)
2. **Railway**
3. **Google Cloud Run**
4. **Heroku**

### Deployment Steps (General):
1. Push the `backend` folder to a GitHub repository or subfolder.
2. Connect your hosting service to the repository.
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn app:app` (you may need to add `gunicorn` to `requirements.txt`).
5. Set environment variables on the hosting platform if needed.
6. Once deployed, update the `VITE_API_URL` in your Firebase frontend deployment.
