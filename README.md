🩺 Healthcare Symptom Checker
This project is an educational tool that uses a Large Language Model (LLM) to provide potential insights based on user-described symptoms. It is built with a modern web architecture featuring a Python backend and a plain HTML/JavaScript frontend.

This application is for informational purposes only and does not provide medical advice.

архитектура
Frontend: A single index.html file using Tailwind CSS for styling. It captures user input and communicates with the backend API.

Backend: A Python API built with FastAPI. It receives requests from the frontend, queries the Gemini LLM, and logs the transaction in a database.

Database: A SQLite database is used to store a history of symptoms and the corresponding AI-generated results.

🚀 How to Run
1. Backend Setup
First, navigate to the backend directory.

cd backend

It's recommended to use a Python virtual environment:

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Now, run the backend server using Uvicorn:

uvicorn main:app --reload

The API will be running at http://127.0.0.1:8000.

2. Frontend Setup
Navigate to the frontend directory and simply open the index.html file in your web browser.

cd frontend
# Then open index.html in Chrome, Firefox, Safari, etc.

You can now use the application. The frontend will automatically connect to the running backend.
