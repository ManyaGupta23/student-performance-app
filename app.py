import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student Intelligence System", layout="wide")

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
page = st.sidebar.radio("📌 Navigation", ["Home","Data Entry","Dashboard","Insights"])

file_name = "student_data.xlsx"

# ---------- HOME ----------
if page == "Home":
    st.title("🎓 Student Intelligence System")
    st.markdown("""
    ### 🚀 Features:
    - Data Entry System  
    - Excel Storage  
    - AI Insights  
    - Interactive Dashboard  
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=200)

# ---------- DATA ENTRY ----------
if page == "Data Entry":

    with st.form("form"):
        st.subheader("📝 Enter Student Details")

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
    df.columns = df.columns.str.strip().str.lower()
    new_data.columns = new_data.columns.astype(str).str.strip().str.lower()
    new_data = new_data.reindex(columns=df.columns, fill_value=0)
    df = pd.concat([df, new_data], ignore_index=True)
else:
    df = new_data
    df.to_excel(file_name, index=False)
    with st.spinner("⏳ Saving..."):
        time.sleep(1)
        st.success("🎉 Data Saved Successfully!")

# ---------- DASHBOARD ----------
if page == "Dashboard":

    if os.path.exists(file_name):
        df = pd.read_excel(file_name)

        st.subheader("📊 Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("👨‍🎓 Students", len(df))
        col2.metric("📘 Avg GPA", round(df["GPA"].mean(),2))
        col3.metric("📉 Avg Absences", round(df["Absences"].mean(),2))

        # ---------- INTERACTIVE CHARTS ----------
        st.subheader("📊 GPA Distribution")
        fig = px.histogram(df, x="GPA")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Gender Distribution")
        fig2 = px.pie(df, names="Gender")
        st.plotly_chart(fig2, use_container_width=True)

        if "GradeClass" in df.columns:
            st.subheader("📈 Grade Distribution")
            fig3 = px.bar(df, x="GradeClass")
            st.plotly_chart(fig3, use_container_width=True)

        st.subheader("🔥 Correlation Heatmap")
        fig4 = px.imshow(df.corr(), text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        st.download_button("📥 Download Data", df.to_csv(index=False), "student_data.csv")

# ---------- INSIGHTS ----------
if page == "Insights":

    if os.path.exists(file_name):
        df = pd.read_excel(file_name)

        last = df.iloc[-1]

        st.subheader("🤖 AI Insights")

        if last["GPA"] < 2:
            st.error("⚠ At Risk Student")
        elif last["GPA"] < 3:
            st.warning("📉 Needs Improvement")
        else:
            st.success("🌟 Excellent Student")

        if last["Absences"] > 10:
            st.warning("📅 High Absences")

        if last["StudyTimeWeekly"] < 10:
            st.info("⏳ Increase Study Time")

        # ---------- COMPARISON ----------
        st.subheader("📈 Performance Comparison")

        fig = px.bar(
            x=["Student GPA","Average GPA"],
            y=[last["GPA"], df["GPA"].mean()]
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success("🙏 Thank You! Keep Learning 🚀")
