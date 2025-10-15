🩺 Health Help: Healthcare Symptom Checker Chatbot
Introduction & Project Context
My name is Shweta Rana, and I am a final-year student at VIT. This project is an assignment I am developing for Unthinkable, and it represents a significant step in my journey from academic knowledge to practical, full-stack application development.

This assignment is teaching me how to integrate foundational skills in HTML/CSS with more complex backend technologies. While I have prior experience with RAG chatbots and LLMs, this project is my first time building and managing a live API, connecting it to a user interface, and structuring it for a real-world use case.

I am grateful to Unthinkable for this insightful and challenging assignment. It is proving to be an invaluable learning experience, and I am excited about the potential for further development and the future possibilities this project holds.

About The Project
This project is an educational tool that uses a Large Language Model (LLM) to provide potential insights based on a conversational exchange with a user about their symptoms. It is built with a modern web architecture featuring a Python backend (FastAPI) and a lightweight HTML/JavaScript frontend.

🏛️ Architecture Overview
The application is designed with a clear separation of concerns between the frontend and backend.

Frontend: A single index.html file styled with Tailwind CSS. It provides a dynamic chat interface that communicates with the backend API.

Backend: A Python API built with FastAPI. It manages conversational context, securely queries the Google Gemini LLM, and logs the chat history.

Database: A SQLite database is used for persistent storage, saving the history of user interactions and AI-generated responses.

🚀 Getting Started ( how to run it on your system)
To run this application locally, you will need to set up and run both the backend and frontend services.

1. Backend Setup
First, navigate to the backend directory.

cd backend

It's highly recommended to use a Python virtual environment:

# Create a virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Before running, you must create a .env file in the backend directory and add your API key:

GEMINI_API_KEY="YOUR_SECRET_API_KEY_GOES_HERE"

Now, run the backend server using Uvicorn:

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

2. Frontend Setup
Navigate to the frontend directory and simply open the index.html file in your preferred web browser.

cd frontend
Then open index.html in Chrome, Firefox, Safari, etc.

The frontend will automatically connect to the running backend service.

💡 Future Scope
Enhanced User Authentication: Implement a user login system to maintain separate chat histories.

Expanded Database: Store more structured data from conversations for potential analysis.

Deployment: Containerize the application with Docker and deploy it to a cloud service.

⚠️ Disclaimer
This application is for educational and informational purposes only and does not provide medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider.
THANK YOU 
