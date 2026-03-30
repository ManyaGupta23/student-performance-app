import streamlit as st
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student AI System", layout="wide")

# ---------- GLASSMORPHISM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #89f7fe, #66a6ff);
}
.glass {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.1);
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎓 Student Performance System</p>', unsafe_allow_html=True)

file_name = "student_data.xlsx"

# ---------- FORM ----------
with st.form("form"):

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 📝 Enter Student Details")

    col1, col2 = st.columns(2)

    with col1:
        Age = st.number_input("Age", 10, 25)
        Gender = st.selectbox("Gender", ["Select","Male","Female"])
        Ethnicity = st.selectbox("Ethnicity", ["Select","Group 0","Group 1"])
        ParentalEducation = st.number_input("Parental Education", 0, 4)
        ParentalSupport = st.number_input("Parental Support", 0, 4)
        StudyTimeWeekly = st.number_input("Study Time", 0.0, 40.0)

    with col2:
        Absences = st.number_input("Absences", 0, 50)
        Tutoring = st.selectbox("Tutoring", ["Select","No","Yes"])
        Extracurricular = st.selectbox("Extracurricular", ["Select","No","Yes"])
        Sports = st.selectbox("Sports", ["Select","No","Yes"])
        Music = st.selectbox("Music", ["Select","No","Yes"])
        Volunteering = st.selectbox("Volunteering", ["Select","No","Yes"])
        GPA = st.number_input("GPA", 0.0, 4.0)

    submit = st.form_submit_button("🚀 Submit")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SAVE ----------
if submit:

    if "Select" in [Gender, Ethnicity, Tutoring, Extracurricular, Sports, Music, Volunteering]:
        st.error("❌ Fill all fields!")
    else:
        new_data = pd.DataFrame({
            "age":[Age],
            "gender":[1 if Gender=="Male" else 0],
            "ethnicity":[1 if Ethnicity=="Group 1" else 0],
            "parentaleducation":[ParentalEducation],
            "parentalsupport":[ParentalSupport],
            "studytime":[StudyTimeWeekly],
            "absences":[Absences],
            "tutoring":[1 if Tutoring=="Yes" else 0],
            "extracurricular":[1 if Extracurricular=="Yes" else 0],
            "sports":[1 if Sports=="Yes" else 0],
            "music":[1 if Music=="Yes" else 0],
            "volunteering":[1 if Volunteering=="Yes" else 0],
            "gpa":[GPA]
        })
        file_name="student_data.xlsx"
        if os.path.exists(file_name):
            df = pd.read_excel(file_name)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_excel(file_name, index=False)

        with st.spinner("⏳ Saving..."):
            time.sleep(1)

        st.success("🎉 Data Saved Successfully!")

# ---------- DASHBOARD ----------
if os.path.exists(file_name):
    df = pd.read_excel(file_name)

    if len(df) > 0:

        st.markdown("## 📊 Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("👨‍🎓 Students", len(df))
        col2.metric("📘 Avg GPA", round(df["GPA"].mean(),2))
        col3.metric("📉 Avg Absences", round(df["Absences"].mean(),2))

        # ---------- PIE CHART ----------
        st.markdown("### 📊 Gender Distribution")
        fig1, ax1 = plt.subplots()
        df["Gender"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax1)
        st.pyplot(fig1)

        # ---------- BAR CHART ----------
        st.markdown("### 📈 Grade Distribution")
        if "GradeClass" in df.columns:
            fig2, ax2 = plt.subplots()
            df["GradeClass"].value_counts().plot(kind="bar", ax=ax2)
            st.pyplot(fig2)

        # ---------- HISTOGRAM ----------
        st.markdown("### 📉 GPA Distribution")
        fig3, ax3 = plt.subplots()
        df["GPA"].hist(ax=ax3)
        st.pyplot(fig3)

        # ---------- PROFILE ----------
        st.markdown("### 🧑‍🎓 Latest Student")

        last = df.iloc[-1]

        st.markdown(f"""
        <div class="glass">
        <h3>Student Profile</h3>
        <p><b>Age:</b> {last['Age']}</p>
        <p><b>Gender:</b> {'Male' if last['Gender']==1 else 'Female'}</p>
        <p><b>GPA:</b> {last['GPA']}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------- DOWNLOAD ----------
        st.download_button(
            "📥 Download Data",
            df.to_csv(index=False),
            "student_data.csv",
            "text/csv"
        )

        st.success("🙏 Thank You! Keep Learning 🚀")
