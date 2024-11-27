import streamlit as st
import joblib
import pandas as pd
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BMI Prediction App",
    page_icon="🏥",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    /* Overall page styling */
    .stApp {
        background: linear-gradient(135deg, #0a192f, #112240, #1a365d, #233554);
        color: #e2e8f0;
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom container styling */
    .custom-container {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 30px;
        padding: 40px;
        margin: 30px 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(100, 255, 218, 0.2);
        backdrop-filter: blur(20px);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .custom-container:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 25px 60px rgba(100, 255, 218, 0.2);
        border-color: rgba(100, 255, 218, 0.4);
    }
    
    /* Headers styling */
    h1 {
        background: linear-gradient(90deg, #64ffda, #00ff88, #64ffda);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 2px;
        animation: shine 4s linear infinite;
        text-transform: uppercase;
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Results container styling */
    .results-container {
        background: linear-gradient(135deg, #1a365d, #233554);
        border-radius: 35px;
        padding: 70px;
        text-align: center;
        margin: 60px 0;
        box-shadow: 0 20px 60px rgba(100, 255, 218, 0.25);
        animation: pulseContainer 3s ease-in-out infinite;
    }
        .results-container h1 {
        color: #64ffda !important;
        -webkit-text-fill-color: #64ffda !important;
        font-size: 42px;
        margin: 20px 0;
    }
    @keyframes pulseContainer {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #64ffda, #00ff88);
        color: #0a192f;
        border-radius: 25px;
        padding: 20px 45px;
        font-weight: 800;
        font-size: 18px;
        border: none;
        transition: all 0.5s ease;
        box-shadow: 0 10px 40px rgba(100, 255, 218, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 45px rgba(100, 255, 218, 0.5);
        background: linear-gradient(45deg, #00ff88, #64ffda);
    }
    
    /* Input elements styling */
    .stSlider, .stSelectbox, .stNumberInput {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(15px);
        transition: all 0.5s ease;
        border: 2px solid rgba(100, 255, 218, 0.15);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider:hover, .stSelectbox:hover, .stNumberInput:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateX(10px);
        border-color: rgba(100, 255, 218, 0.4);
        box-shadow: 0 12px 35px rgba(100, 255, 218, 0.2);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stApp > * {
        animation: fadeInUp 1s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Load the model
def load_model():
    with open('random_forest_model.pkl', 'rb') as file:
        return joblib.load(file)

model = load_model()

# Modern header
st.markdown('<h1 style="text-align: center;">🏥 BMI Prediction System</h1>', unsafe_allow_html=True)

# Description
st.markdown("""
    <div class="custom-container">
        <h3>Welcome to BMI Prediction System</h3>
        <p>This intelligent system predicts BMI category based on your lifestyle factors. 
        Fill in your information below for an accurate prediction.</p>
    </div>
""", unsafe_allow_html=True)

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("👤 Personal Info")
    Gender = st.selectbox('Gender', ['Female', 'Male'])
    Age = st.number_input('Age', min_value=0, max_value=100, value=20, step=1)
    Height = st.number_input('Height (m)', min_value=0.00, max_value=2.00, value=1.50, step=0.01)

with col2:
    st.subheader("⚖️ Physical Metrics")
    Weight = st.number_input('Weight (kg)', min_value=0.0, max_value=200.0, value=50.0, step=0.1)
    Fam_overweight = st.selectbox('Family History of Overweight', ['Yes', 'No'])
    FAVC = st.selectbox('High Calorie Food Frequency', ['Yes', 'No'])

with col3:
    st.subheader("🍽️ Eating Habits")
    FCVC = st.number_input('Vegetable Consumption (0-3)', min_value=0, max_value=3, value=1)
    NCP = st.number_input('Main Meals per Day', min_value=0, max_value=10, value=3)
    CAEC = st.selectbox('Between Meals Consumption', ['Always', 'Frequently', 'Sometimes', 'No'])

# Lifestyle factors
st.markdown('<div class="custom-container"><h3 style="font-size: 50px; text-align: center;">🌟 Lifestyle Factors</h3></div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    SMOKE = st.selectbox('Smoking Status', ['Yes', 'No'], help='Do you smoke?')
    CH2O = st.number_input('Daily Water Consumption (L)', min_value=0.0, max_value=3.0, value=1.0, step=0.1, help='How much water do you drink daily?')

with col5:
    SCC = st.selectbox('Calorie Monitoring', ['Yes', 'No'], help='Do you monitor your calorie intake?')
    FAF = st.number_input('Physical Activity (0-3)', min_value=0, max_value=3, value=1, help='How active are you?')
    MTRANS = st.selectbox('Transportation Mode', ['Automobile', 'Motorbike', 'Bike', 'Public Transportation', 'Walking'])


with col6:
    TUE = st.number_input('Technology Use Time (0-3)', min_value=0, max_value=3, value=1, help='How much time do you spend using technology?')
    CALC = st.selectbox('Alcohol Consumption', ['Always', 'Frequently', 'Sometimes', 'No'], help='How often do you drink alcohol?')

st.markdown('</div>', unsafe_allow_html=True)

# Calculate BMI
BMI = Weight / (Height ** 2)
# The rest of your data processing code remains the same
input_data = pd.DataFrame({
    'Gender': [1 if Gender == 'Male' else 0],
    'Age': [np.log(Age)],
    'Height': [Height],
    'family_history_with_overweight': [1 if Fam_overweight == 'Yes' else 0],
    'FAVC': [1 if FAVC == 'Yes' else 0],
    'FCVC': [FCVC],
    'NCP': [NCP],
    'CAEC': [0 if CAEC == 'Always' else 1 if CAEC == 'Frequently' else 2 if CAEC == 'Sometimes' else 3],
    'SMOKE': [1 if SMOKE == 'Yes' else 0],
    'CH2O': [CH2O],
    'SCC': [1 if SCC == 'Yes' else 0],
    'FAF': [FAF],
    'TUE': [TUE],
    'CALC': [0 if CALC == 'Always' else 1 if CALC == 'Frequently' else 2 if CALC == 'Sometimes' else 3],
    'MTRANS': [0 if MTRANS == 'Automobile' else 1 if MTRANS == 'Bike' else 2 if MTRANS == 'Motorbike' else 3 if MTRANS == 'Public Transportation' else 4],
    'BMI': [BMI]
})

with open('label_mappings.json', 'r') as file:
    label_encoders = json.load(file)

if st.button('Get Your BMI Prediction', key='predict_button', help='Click to get your BMI prediction'):
    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)[0]
    result = list(label_encoders["NObeyesdad"].keys())[prediction[0]].replace('_', ' ')
    probability = probabilities[prediction[0]]  # Getting the probability of the predicted class
    
    st.markdown(f"""
        <div class="results-container">
            <h2>Your Weight Category</h2>
            <h1>{result} ({probability * 100:.2f}%)</h1>
            <p>Based on your provided information</p>
        </div>
    """, unsafe_allow_html=True)

# Footer and Social Media Links
st.markdown("""
    <div style="
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 15px;
        border-top: 2px solid rgba(100, 255, 218, 0.2);
        animation: fadeIn 1s ease-in;
    ">
        <p style="
            font-size: 16px;
            color: #64ffda;
            letter-spacing: 2px;
            font-weight: 500;
            margin: 0;
        ">
            <span style="animation: pulse 2s infinite">💫</span> 
            Crafted with passion by Hubblemind • Abie Nugraha 
            <span style="animation: pulse 2s infinite">💫</span>
        </p>
        <p style="
            font-size: 14px;
            color: #8892b0;
            margin-top: 5px;
        ">© 2024</p>
        <div style="margin-top: 20px;">
            <a href="https://www.linkedin.com/in/aabienugraha/" target="_blank" style="
                text-decoration: none;
                margin: 0 10px;
            ">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" height="30" />
            </a>
            <a href="mailto:aabienugraha@gmail.com" style="
                text-decoration: none;
                margin: 0 10px;
            ">
                <img src="https://cdn-icons-png.flaticon.com/512/5968/5968534.png" width="30" height="30" />
            </a>
            <a href="https://www.instagram.com/nugbie_/profilecard/" target="_blank" style="
                text-decoration: none;
                margin: 0 10px;
            ">
                <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="30" height="30" />
            </a>
        </div>
    </div>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)
