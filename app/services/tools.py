import sqlite3
import random
import datetime
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# Database Setup
conn = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialty TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    doctor_id INTEGER,
    appointment_time TEXT,
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    amount REAL,
    payment_method TEXT,
    transaction_id TEXT,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS hospital_pharmacy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT UNIQUE,
    quantity INTEGER
)
""")

conn.commit()

# 1️⃣ **Tool: Get Available Doctors**
@tool
def get_doctor_list() -> str:
    """Returns a list of available doctors and their specialties."""
    conn = sqlite3.connect("hospital.db",check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM doctors")
    doctors = cursor.fetchall()
    
    if not doctors:
        return "❌ No doctors available at the moment."
    
    doctor_list = "\n".join([f"👨‍⚕️ Dr. {doc[1]} - {doc[2]} (ID: {doc[0]})" for doc in doctors])
    return f"✅ Available Doctors:\n{doctor_list}"

# 2️⃣ **Tool: Book Doctor Appointment**
@tool
def book_doctor_appointment(patient_id: str, doctor_id: int, appointment_time: str) -> str:
    """Books an appointment with a doctor for a patient."""
    cursor.execute("SELECT name FROM doctors WHERE id=?", (doctor_id,))
    doctor = cursor.fetchone()

    if not doctor:
        return "❌ Invalid Doctor ID. Please check the available doctors list."

    cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_time) VALUES (?, ?, ?)",
                   (patient_id, doctor_id, appointment_time))
    conn.commit()

    return (f"✅ Appointment booked successfully!\n"
            f"👨‍⚕️ Doctor: Dr. {doctor[0]}\n"
            f"🩺 Appointment Time: {appointment_time}")

# 3️⃣ **Tool: Pay Medical Bill**
@tool
def pay_medical_bill(patient_id: str, amount: float, payment_method: str) -> str:
    """Processes medical bill payment for a patient."""
    if amount <= 0:
        return "❌ Invalid amount. Please enter a valid amount."

    # Generate transaction ID
    transaction_id = f"TXN-{random.randint(100000, 999999)}"
    payment_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store payment record in database
    cursor.execute("INSERT INTO payments (patient_id, amount, payment_method, transaction_id, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (patient_id, amount, payment_method, transaction_id, payment_time))
    conn.commit()

    return (f"✅ Payment of ${amount} for Patient ID {patient_id} has been successfully processed.\n"
            f"💳 Payment Method: {payment_method}\n"
            f"📄 Transaction ID: {transaction_id}\n"
            f"🕒 Payment Time: {payment_time}")

# 4️⃣ **Tool: Check Medicine Availability in Hospital Pharmacy**
@tool
def check_hospital_medicine_availability(medicine_name: str) -> str:
    """Checks the availability of a medicine in the hospital pharmacy."""
    
    # Ensure the first letter is capitalized
    formatted_medicine_name = medicine_name.capitalize()
    
    try:
        # Ensure the cursor is properly connected to the database
        cursor.execute("SELECT quantity FROM hospital_pharmacy WHERE medicine_name = ?", (formatted_medicine_name,))
        
        result = cursor.fetchone()

        if not result:
            return f"❌ {formatted_medicine_name} is not available in the hospital pharmacy."
        
        # Debug output to ensure that the result is fetched
        print(f"Database result for {formatted_medicine_name}: {result}")

        quantity = result[0]

        if quantity > 0:
            return f"✅ {formatted_medicine_name} is available in stock. Quantity: {quantity}."
        else:
            return f"⚠️ {formatted_medicine_name} is currently out of stock."

    except Exception as e:
        return f"❌ Error occurred while checking the medicine: {str(e)}"

    
# Initialize OpenAI agent for patient symtem checkers
@tool
def patient_symptom_checker(user_input: str) -> str:
    """Initiates a conversation with the OpenAI agent for patient symptom checking."""
    prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a professional medical assistant chatbot. Your role is to help patients by checking symptoms "
     "and providing general health advice based on medical knowledge. "
     "You ask follow-up questions to gather more details about the patient's symptoms, such as duration, severity, and related issues. "
     "Based on the patient's responses, you suggest possible health conditions and whether they should seek medical attention. "
     "You do NOT give a final diagnosis or prescribe medication. "
     "If symptoms seem serious, strongly advise the user to consult a doctor immediately."),
    ("human", "{input}"),
    ])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        max_tokens=100,
        temperature=0.2)
    chain = prompt | llm
    response = chain.invoke({"input":user_input,})  # Invoke LLM with user input
    #print(response)

    return response.content