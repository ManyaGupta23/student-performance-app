import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("🎓 Student Performance Prediction System")

# Load dataset
data = pd.read_excel("student_data.xlsx")
data.columns = data.columns.str.lower()

# Train model
X = data[['studytimeweekly', 'absences', 'parentalsupport']]
y = data['gpa']

model = LinearRegression()
model.fit(X, y)

# User Inputs
st.sidebar.header("Enter Student Details")

studytime = st.sidebar.slider("Study Time (hours/week)", 0.0, 20.0, 5.0)
absences = st.sidebar.slider("Absences", 0, 30, 5)
support = st.sidebar.slider("Parental Support (0-5)", 0, 5, 2)

# Prediction
input_data = pd.DataFrame({
    'studytimeweekly': [studytime],
    'absences': [absences],
    'parentalsupport': [support]
})

predicted_gpa = model.predict(input_data)[0]

st.subheader("📊 Prediction Result")
st.write("Predicted GPA:", round(predicted_gpa, 2))

# Risk Level
if predicted_gpa < 2:
    st.error("⚠ High Risk")
elif predicted_gpa < 3:
    st.warning("⚠ Medium Risk")
else:
    st.success("✅ Low Risk")

# Show dataset (optional)
if st.checkbox("Show Dataset"):
    st.write(data.head())