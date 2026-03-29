import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student Performance System", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2f3, #ffffff);
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<p class="title">🎓 Student Performance Prediction System</p>', unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📤 Upload Student Dataset (Excel)", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Remove ID
    if "studentid" in df.columns:
        df = df.drop("studentid", axis=1)

    if "gradeclass" not in df.columns:
        st.error("❌ 'gradeclass' column missing!")
        st.stop()

    X = df.drop("gradeclass", axis=1)
    y = df["gradeclass"]

    # ---------- PROGRESS BAR ----------
    progress = st.progress(0)

    with st.spinner("⏳ Training model..."):
        for i in range(100):
            progress.progress(i + 1)

        model = RandomForestClassifier()
        model.fit(X, y)

    st.success("✅ Model trained successfully!")

    # ---------- ACCURACY ----------
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)

    st.metric("🎯 Model Accuracy", f"{round(acc*100,2)}%")

    # ---------- INPUT FORM ----------
    st.markdown("## 📝 Enter Student Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 10, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        ethnicity = st.selectbox("Ethnicity", ["Group 0", "Group 1"])
        parentaleducation = st.slider("Parental Education", 0, 4)
        parentalsupport = st.slider("Parental Support", 0, 4)
        studytime = st.slider("Study Time (hrs/week)", 0.0, 40.0)

    with col2:
        absences = st.slider("Absences", 0, 50)
        tutoring = st.selectbox("Tutoring", ["No", "Yes"])
        extracurricular = st.selectbox("Extracurricular", ["No", "Yes"])
        sports = st.selectbox("Sports", ["No", "Yes"])
        music = st.selectbox("Music", ["No", "Yes"])
        volunteering = st.selectbox("Volunteering", ["No", "Yes"])
        gpa = st.slider("GPA", 0.0, 4.0)

    # ---------- INPUT DATA ----------
    input_data = pd.DataFrame({
        "age":[age],
        "gender":[1 if gender=="Male" else 0],
        "ethnicity":[1 if ethnicity=="Group 1" else 0],