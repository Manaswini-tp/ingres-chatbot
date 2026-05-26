# ingres-chatbot

# 🌊 INGRES AI Chatbot

An intelligent, multilingual chatbot for accessing Indian groundwater data. The system provides real-time information about rainfall, groundwater extraction stages, recharge data, and availability across Indian states and districts.

## 🚀 Features

- **🤖 AI-Powered Conversations**: Uses Rasa NLU for intent recognition and entity extraction
- **🌐 Multilingual Support**: English, Hindi, Kannada, Telugu, Tamil, Marathi, Bengali, Gujarati
- **📊 Data Visualization**: Interactive charts for rainfall distribution, extraction stages, and comparisons
- **🔍 Smart Location Detection**: Recognizes state/district names in multiple languages and variations
- **💡 Suggested Queries**: Context-aware recommendations for follow-up questions
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **FastAPI** - REST API framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Rasa** - NLU and dialogue management
- **Deep-Translator** - Multi-language translation

### Frontend
- **React 18** - UI framework
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **React Icons** - Icon library

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- pip and npm

## 🔧 Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/ingres-ai-chatbot.git
cd ingres-ai-chatbot

### 2. Backend Setup

cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Create a .env file in the backend directory:
DATABASE_URL=postgresql://username:password@localhost:5432/ingres_db

### 3. Database Setup

# Create PostgreSQL database
createdb ingres_db

# Run migrations (tables are auto-created on startup)
### 4. Frontend Setup

cd frontend
npm install
### 5. Rasa Setup

cd rasa
pip install -r requirements.txt

# Train the Rasa model
rasa train

# Start Rasa actions server (in a separate terminal)
rasa run actions

# Start Rasa server (in another terminal)
rasa run --enable-api --cors "*"

## 🏃 Running the Application
Start Backend Server

cd backend
uvicorn app.main:app --reload --port 8000
The API will be available at http://localhost:8000

# Start Frontend Development Server

cd frontend
npm start
The app will open at http://localhost:3000

📁 Project Structure

ingres-chatbot/
├── backend/
│   ├── app/
│   │   ├── crud.py           # Database operations
│   │   ├── database.py       # DB connection
│   │   ├── data_processor.py # Excel data loader
│   │   ├── main.py           # FastAPI routes
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── translation.py    # Multi-language service
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartDisplay.jsx
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── DataCard.jsx
│   │   │   ├── InputBar.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── rasa/
│   ├── actions/
│   │   └── actions.py
│   ├── data/
│   │   ├── nlu.yml
│   │   ├── rules.yml
│   │   └── stories.yml
│   ├── config.yml
│   ├── credentials.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   └── requirements.txt
└── README.md

## 🔌 API Endpoints
Method	Endpoint	Description
POST	/chat	Send a message to the chatbot
GET	/states	Get all available states
GET	/districts/{state}	Get districts for a state
GET	/data/{state}	Get all data for a state
GET	/stats/{state}	Get statistics for a state
GET	/stats/total	Get overall statistics
GET	/health	Health check

## Chat Request Example
json
{
  "message": "What is the rainfall in Bangalore?",
  "language": "en"
}

## 📊 Data Source
The application loads groundwater data from an Excel file (ingres-data.xlsx) with the following columns:

STATE, DISTRICT
Rainfall (mm)
Ground Water Recharge (ham)
Stage of Ground Water Extraction (%)
Net Annual Ground Water Availability (ham)

Place the Excel file in the backend/ directory before starting the server.

## 🌍 Supported Languages
Code	Language
en	English
hi	Hindi
kn	Kannada
te	Telugu
ta	Tamil
mr	Marathi
bn	Bengali
gu	Gujarati

## 🐛 Troubleshooting
Database Connection Issues
Ensure PostgreSQL is running
Verify credentials in .env file
Create the database manually if needed
Rasa Connection Issues
Start Rasa actions server first: rasa run actions
Then start Rasa server: rasa run --enable-api --cors "*"
Check port 5005 is available
Frontend Can't Connect to Backend
Ensure backend is running on port 8000
Check CORS settings in main.py

### 📝 License
This project is licensed under the MIT License.

🙏 Acknowledgments
INGRES (Indian Groundwater Resource Estimation System) for data standards (https://ingres.iith.ac.in/home)
Rasa for NLU capabilities
FastAPI community

💧 Made with love for sustainable water management
