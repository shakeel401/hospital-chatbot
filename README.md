# Hospital Chatbot Backend (FastAPI)

## Overview
This project is a FastAPI-based hospital chatbot that integrates AI-powered interactions with hospital services. It leverages **LangGraph** for agentic behavior and **MemorySaver** for persistent interactions. The chatbot can:

- Retrieve a list of available doctors
- Book doctor appointments
- Process medical bill payments
- Check hospital pharmacy medicine availability
- Perform patient symptom checks using AI

## Features
### ✅ AI-Powered Conversational Agent
- Uses **LangGraph** for managing conversational states and decision-making.
- Implements **MemorySaver** to store chat history and ensure smooth interactions.
- Uses **ChatOpenAI (GPT-4o-mini)** to generate responses.

### 🏥 Hospital Management Functions
- **Doctor Listing:** Fetches available doctors and their specialties.
- **Appointment Booking:** Schedules appointments with doctors.
- **Medical Bill Payment:** Handles patient payments and generates transaction IDs.
- **Pharmacy Stock Check:** Checks medicine availability in the hospital database.
- **Symptom Checker:** Uses AI to assist patients by analyzing symptoms and recommending next steps.

## Tech Stack
- **FastAPI**: Lightweight and high-performance backend framework.
- **LangChain & LangGraph**: Manages agentic workflows and decision-making.
- **SQLite**: Stores doctors, appointments, payments, and pharmacy data.
- **OpenAI GPT-4o-mini**: Provides intelligent chatbot responses.
- **MemorySaver**: Ensures chat memory is preserved across interactions.

## Installation
### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)

### Steps to Run Locally
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/hospital-chatbot.git
   cd hospital-chatbot
   ```
2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run FastAPI Server**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Access API Documentation**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/chat` | Processes user input and returns chatbot response |

### Example API Request
```json
{
    "user_input": "Paracetamol is available in hospital pharmacy?",
    "thread_id": "12345"
}
```

### Example Response
```json
{
    "bot_message": "Paracetamol is available in the hospital pharmacy, with a stock quantity of 150."
}
```

## LangGraph Agentic Functions
### 🔄 Conversational Flow
- **StateGraph** is used to manage dialogue flow.
- **ToolNode** executes hospital-related tools dynamically.
- **Conditional edges** ensure smooth transitions between chatbot responses and tool executions.

### 🧠 Memory Management
- **MemorySaver** allows storing previous interactions for contextual awareness.
- Each conversation is associated with a `thread_id` to maintain continuity.

## Database Schema (SQLite)
### `doctors` Table
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| name | TEXT |
| specialty | TEXT |

### `appointments` Table
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| patient_id | TEXT |
| doctor_id | INTEGER (FK) |
| appointment_time | TEXT |

### `payments` Table
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| patient_id | TEXT |
| amount | REAL |
| payment_method | TEXT |
| transaction_id | TEXT |
| timestamp | TEXT |

### `hospital_pharmacy` Table
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| medicine_name | TEXT UNIQUE |
| quantity | INTEGER |

## Future Improvements
- Implement user authentication and role-based access.
- Integrate **Twilio** or **WhatsApp API** for real-time communication.
- Enhance AI capabilities for better symptom analysis.
- Deploy using **Docker & Kubernetes**.

---
### 🚀 Ready to Build?
Start the FastAPI server and explore the AI-powered hospital chatbot!

