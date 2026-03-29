import streamlit as st
import pandas as pd
import os
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student AI System", layout="wide")

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #dfe9f3, #ffffff);
}
.big-title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #2c3e50;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------- LOADING ----------
progress = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress.progress(i+1)

st.markdown('<p class="big-title">🎓 Student Performance AI System</p>', unsafe_allow_html=True)

# ---------- FILE ----------
file_name = "student_data.xlsx"

if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=[
        "age","gender","ethnicity","parentaleducation","parentalsupport",
        "studytime","absences","tutoring","extracurricular","sports",
        "music","volunteering","gpa","gradeclass"
    ])

# ---------- MODEL ----------
model = None
if len(df) > 5:
    X = df.drop("gradeclass", axis=1)
    y = df["gradeclass"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    colA, colB, colC = st.columns(3)
    colA.metric("📊 Records", len(df))
    colB.metric("🎯 Accuracy", f"{round(acc*100,2)}%")
    colC.metric("📈 Features", len(X.columns))

# ---------- DASHBOARD ----------
if len(df) > 0:
    st.markdown("## 📊 Advanced Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        df["gpa"].hist(ax=ax1)
        ax1.set_title("GPA Distribution")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        df["studytime"].hist(ax=ax2)
        ax2.set_title("Study Time Distribution")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        fig3, ax3 = plt.subplots()
        df["absences"].hist(ax=ax3)
        ax3.set_title("Absences")
        st.pyplot(fig3)

    with col4:
        fig4, ax4 = plt.subplots()
        df["gradeclass"].value_counts().plot(kind="bar", ax=ax4)
        ax4.set_title("Grade Distribution")
        st.pyplot(fig4)

# ---------- DOWNLOAD ----------
if len(df) > 0:
    st.download_button(
        label="📥 Download Dataset",
        data=df.to_csv(index=False),
        file_name="student_data.csv",
        mime="text/csv"
    )

# ---------- INPUT FORM ----------
st.markdown("## 📝 Enter Student Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 10, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ethnicity = st.selectbox("Ethnicity", ["Group 0", "Group 1"])
    parentaleducation = st.slider("Parental Education", 0, 4)
    parentalsupport = st.slider("Parental Support", 0, 4)
    studytime = st.slider("Study Time", 0.0, 40.0)

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
    "parentaleducation":[parentaleducation],
    "parentalsupport":[parentalsupport],
    "studytime":[studytime],
    "absences":[absences],
    "tutoring":[1 if tutoring=="Yes" else 0],
    "extracurricular":[1 if extracurricular=="Yes" else 0],
    "sports":[1 if sports=="Yes" else 0],
    "music":[1 if music=="Yes" else 0],
    "volunteering":[1 if volunteering=="Yes" else 0],
    "gpa":[gpa]
})

# ---------- PREDICT ----------
if st.button("🚀 Predict & Save"):

    if model is None:
        st.error("❌ Not enough data to train model")
    else:
        input_data = input_data.reindex(columns=X.columns, fill_value=0)

        pred = model.predict(input_data)[0]

        grade_map = {4:"A",3:"B",2:"C",1:"D",0:"F"}
        grade = grade_map[pred]

        st.success(f"🎯 Predicted Grade: {grade}")

        # Save
        input_data["gradeclass"] = pred
        df = pd.concat([df, input_data], ignore_index=True)
        df.to_excel(file_name, index=False)

        # ---------- RESULT GRAPH ----------
        st.markdown("## 📊 Result Visualization")

        fig5, ax5 = plt.subplots()
        ax5.bar(["GPA","Study Time","Absences"], [gpa, studytime, absences])
        ax5.set_title("Student Performance Indicators")
        st.pyplot(fig5)

        st.success("🙏 Thank You! Keep Growing 🚀")
