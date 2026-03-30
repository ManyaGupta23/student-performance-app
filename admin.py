import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1e3c72, #2a5298);
    color: white;
}
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN SYSTEM ----------
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if not st.session_state.admin_logged:
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.admin_logged = True
            st.success("✅ Login Successful")
        else:
            st.error("❌ Invalid Credentials")

    st.stop()

# ---------- MAIN DASHBOARD ----------
st.title("⚙ Admin Dashboard")

file_name = "student_data.xlsx"

# ---------- CHECK FILE ----------
if os.path.exists(file_name):

    df = pd.read_excel(file_name)

    # Clean columns
    df.columns = df.columns.astype(str).str.strip().str.lower()

    if len(df) > 0:

        # ---------- METRICS ----------
        st.markdown("## 📊 System Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("👨‍🎓 Total Students", len(df))
        col2.metric("📘 Avg GPA", round(df["GPA"].mean(), 2))
        col3.metric("📉 Avg Absences", round(df["Absences"].mean(), 2))

        # ---------- DATA TABLE ----------
        st.markdown("## 📂 Student Data")
        st.dataframe(df, use_container_width=True)

        # ---------- FILTER ----------
        st.markdown("## 🔍 Filter Data")

        min_GPA = st.slider("Minimum GPA", 0.0, 4.0, 0.0)
        max_Absences = st.slider("Max Absences", 0, 50, 50)

        filtered_df = df[(df["GPA"] >= min_GPA) & (df["Absences"] <= max_Absences)]

        st.write("Filtered Data:")
        st.dataframe(filtered_df, use_container_width=True)

        # ---------- CHARTS ----------
        st.markdown("## 📊 Analytics")

        # GPA Distribution
        fig1 = px.histogram(df, x="GPA", title="GPA Distribution")
        st.plotly_chart(fig1, use_container_width=True)

        # Gender Pie
        fig2 = px.pie(df, names="Gender", title="Gender Ratio")
        st.plotly_chart(fig2, use_container_width=True)

        # Absences vs GPA
        fig3 = px.scatter(df, x="Absences", y="GPA", title="Absences vs GPA")
        st.plotly_chart(fig3, use_container_width=True)

        # Heatmap (numeric only)
        st.markdown("### 🔥 Correlation Heatmap")
        fig4 = px.imshow(df.select_dtypes(include='number').corr(), text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        # ---------- DOWNLOAD ----------
        st.markdown("## 📥 Download Data")

        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="student_data.csv",
            mime="text/csv"
        )

        # ---------- DELETE ----------
        st.markdown("## ⚠ Danger Zone")

        if st.button("🗑 Delete All Data"):
            os.remove(file_name)
            st.success("All data deleted successfully!")
            st.experimental_rerun()

    else:
        st.warning("⚠ File exists but no data inside!")

else:
    st.error("❌ No data file found. Please add data from User App.")