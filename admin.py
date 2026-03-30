import streamlit as st
import pandas as pd
import os
import plotly.express as px
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Edu Intelligence - Admin", layout="wide")

file_name = "student_data.xlsx"

# ---------- GLASS LOGIN UI ----------
st.markdown("""
<style>

/* Animated background */
.stApp {
    background: linear-gradient(-45deg, #1f1c2c, #928dab, #2b5876, #4e4376);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}

/* Animation */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass card */
.login-card {
    background: rgba(255,255,255,0.1);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Input fields */
.stTextInput input {
    background-color: rgba(255,255,255,0.9) !important;
    color: black !important;
    border-radius: 10px;
}

/* Button */
.stButton button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white !important;
    border-radius: 10px;
    font-size: 16px;
}

/* Labels */
label {
    color: white !important;
}

/* Dashboard cards */
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ---------- LOGIN ----------
if not st.session_state.admin_logged:

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("<h1 style='color:white;'>🎓 Edu Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#ddd;'>Admin Login Panel</p>", unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🚀 Login"):

        with st.spinner("Authenticating..."):
            time.sleep(1.2)

        if username == "admin" and password == "1234":
            st.success("✅ Login Successful")
            st.session_state.admin_logged = True
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------- LOGOUT ----------
if st.sidebar.button("🚪 Logout"):
    st.session_state.admin_logged = False
    st.rerun()

# ---------- DASHBOARD ----------
st.title("⚙ Admin Dashboard")
file_name="student_data.xlsx"
if os.path.exists(file_name):

    df = pd.read_excel(file_name)

    # Safe column cleaning
    df.columns = df.columns.astype(str).str.strip().str.lower()

    if len(df) > 0:

        st.markdown("## 📊 Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("👨‍🎓 Students", len(df))
        col2.metric("📘 Avg GPA", round(df["gpa"].mean(), 2))
        col3.metric("📉 Avg Absences", round(df["absences"].mean(), 2))

        # ---------- TABLE ----------
        st.markdown("## 📂 Student Data")
        st.dataframe(df, use_container_width=True)

        # ---------- FILTER ----------
        st.markdown("## 🔍 Filter")

        min_gpa = st.slider("Minimum GPA", 0.0, 4.0, 0.0)
        max_abs = st.slider("Max Absences", 0, 50, 50)

        filtered_df = df[(df["gpa"] >= min_gpa) & (df["absences"] <= max_abs)]

        st.dataframe(filtered_df, use_container_width=True)

        # ---------- CHARTS ----------
        st.markdown("## 📊 Analytics")

        fig1 = px.histogram(df, x="gpa", title="GPA Distribution")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(df, names="gender", title="Gender Distribution")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(df, x="studytime", y="gpa", title="Study Time vs GPA")
        st.plotly_chart(fig3, use_container_width=True)

        # Heatmap safe
        st.markdown("### 🔥 Correlation Heatmap")
        fig4 = px.imshow(df.select_dtypes(include='number').corr(), text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        # ---------- DOWNLOAD ----------
        st.download_button(
            "📥 Download Data",
            df.to_csv(index=False),
            "student_data.csv"
        )

        # ---------- DELETE ----------
        st.markdown("## ⚠ Danger Zone")

        if st.button("🗑 Delete All Data"):
            os.remove(file_name)
            st.success("All data deleted!")
            st.rerun()

    else:
        st.warning("⚠ File exists but no data inside")

else:
    st.error("❌ No data file found. Please use User App first.")
