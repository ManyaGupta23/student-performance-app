import io
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# --- Header ---
st.markdown("""
<h1 style='text-align:center; color:#4B0082;'>🎓 Student Performance Dashboard</h1>
<p style='text-align:center; color:#666;'>Predict, Analyze & Export Student Performance</p>
""", unsafe_allow_html=True)

# --- Load Training Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("student_data.xlsx")
    return df

df = load_data()

# --- Encode categorical variables ---
le_ethnicity = LabelEncoder()
le_parent = LabelEncoder()
le_tutoring = LabelEncoder()
le_parentsupport = LabelEncoder()
le_extracurricular = LabelEncoder()
le_gradeclass = LabelEncoder()

df['Ethnicity_enc'] = le_ethnicity.fit_transform(df['Ethnicity'])
df['ParentalEducation_enc'] = le_parent.fit_transform(df['ParentalEducation'])
df['Tutoring_enc'] = le_tutoring.fit_transform(df['Tutoring'])
df['ParentalSupport_enc'] = le_parentsupport.fit_transform(df['ParentalSupport'])
df['Extracurricular_enc'] = le_extracurricular.fit_transform(df['Extracurricular'])
df['GradeClass_enc'] = le_gradeclass.fit_transform(df['GradeClass'])

# --- Features & Target ---
X = df[['Age','Ethnicity_enc','ParentalEducation_enc','StudyTimeWeekly','Absences',
        'Tutoring_enc','ParentalSupport_enc','Extracurricular_enc','Sports','Music','Volunteering']]
y_gpa = df['GPA']
y_grade = df['GradeClass_enc']

# --- Train Models ---
model_gpa = RandomForestRegressor(n_estimators=100, random_state=42)
model_gpa.fit(X, y_gpa)

model_grade = RandomForestClassifier(n_estimators=100, random_state=42)
model_grade.fit(X, y_grade)

# --- Sidebar Navigation ---
st.sidebar.title("Dashboard Menu")
menu = st.sidebar.radio("Go to:", ["Home","Prediction","Insights","Prediction History"])

# --- In-Memory History ---
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Datetime','Age','Ethnicity','ParentalEducation',
                                                     'StudyTimeWeekly','Absences','Tutoring','ParentalSupport',
                                                     'Extracurricular','Sports','Music','Volunteering',
                                                     'Predicted_GPA','Predicted_GradeClass'])

# --- HOME ---
if menu == "Home":
    st.subheader("Welcome to the Student Performance Dashboard")
    st.write("Use this dashboard to predict student GPA and GradeClass, visualize insights, and export predictions.")
    st.write("Navigate to the **Prediction** tab to enter student details.")

# --- PREDICTION ---
elif menu == "Prediction":
    st.subheader("Enter Student Details for Prediction")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 10, 25, 16)
        ethnicity = st.selectbox("Ethnicity", df['Ethnicity'].unique())
        parental_ed = st.selectbox("Parental Education", df['ParentalEducation'].unique())
        study_time = st.number_input("Study Time Weekly (hrs)", 0, 50, 10)
        absences = st.number_input("Absences", 0, 50, 2)
        tutoring = st.selectbox("Tutoring", df['Tutoring'].unique())
    with col2:
        parentsupport = st.selectbox("Parental Support", df['ParentalSupport'].unique())
        extracurricular = st.selectbox("Extracurricular Activities", df['Extracurricular'].unique())
        sports = st.number_input("Sports (hrs/week)", 0, 20, 2)
        music = st.number_input("Music (hrs/week)", 0, 20, 1)
        volunteering = st.number_input("Volunteering (hrs/week)", 0, 20, 0)

    if st.button("Predict"):
        input_df = pd.DataFrame({
            'Age':[age],
            'Ethnicity_enc':[le_ethnicity.transform([ethnicity])[0]],
            'ParentalEducation_enc':[le_parent.transform([parental_ed])[0]],
            'StudyTimeWeekly':[study_time],
            'Absences':[absences],
            'Tutoring_enc':[le_tutoring.transform([tutoring])[0]],
            'ParentalSupport_enc':[le_parentsupport.transform([parentsupport])[0]],
            'Extracurricular_enc':[le_extracurricular.transform([extracurricular])[0]],
            'Sports':[sports],
            'Music':[music],
            'Volunteering':[volunteering]
        })

        pred_gpa = model_gpa.predict(input_df)[0]
        pred_grade = le_gradeclass.inverse_transform(model_grade.predict(input_df))[0]

        st.balloons()
        st.success(f"🎯 Predicted GPA: {round(pred_gpa,2)}")
        st.success(f"🎓 Predicted GradeClass: {pred_grade}")

        # Save to history
        new_entry = {
            'Datetime': datetime.now(),
            'Age': age, 'Ethnicity': ethnicity, 'ParentalEducation': parental_ed,
            'StudyTimeWeekly': study_time, 'Absences': absences, 'Tutoring': tutoring,
            'ParentalSupport': parentsupport, 'Extracurricular': extracurricular,
            'Sports': sports, 'Music': music, 'Volunteering': volunteering,
            'Predicted_GPA': round(pred_gpa,2), 'Predicted_GradeClass': pred_grade
        }
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_entry])], ignore_index=True)

        # Download prediction
            # 1. Convert your dictionary into a DataFrame
            df_to_download = pd.DataFrame([new_entry])

           # 2. Create a memory buffer (a "virtual file")
           buffer = io.BytesIO()

           # 3. Write the Excel data into that virtual file
           with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
               df_to_download.to_excel(writer, index=False, sheet_name='Prediction')

           # 4. Provide the data to the Streamlit button
           st.download_button(
                label="👉 Download This Prediction as Excel",
                data=buffer.getvalue(), # This gets the actual data out of the buffer
                file_name="student_prediction.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
               )
# --- INSIGHTS ---
elif menu == "Insights":
    st.subheader("📊 Dataset Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df['GPA'])
        st.bar_chart(df['StudyTimeWeekly'])
    with col2:
        st.bar_chart(df['Absences'])
        st.bar_chart(df['Volunteering'])

    st.subheader("🏆 Top Students by GPA")
    st.dataframe(df.nlargest(5,'GPA')[['StudentID','GPA','GradeClass','StudyTimeWeekly']])

    st.subheader("📈 Average Metrics")
    st.metric("Average GPA", round(df['GPA'].mean(),2))
    st.metric("Average Study Hours", round(df['StudyTimeWeekly'].mean(),2))
    st.metric("Average Absences", round(df['Absences'].mean(),2))

# --- PREDICTION HISTORY ---
elif menu == "Prediction History":
    st.subheader("📝 Prediction History")
    if st.session_state.history.empty:
        st.info("No predictions made yet!")
    else:
        st.dataframe(st.session_state.history)
        
        # Proper Excel download
        from io import BytesIO
        to_download = BytesIO()
        st.session_state.history.to_excel(to_download, index=False)
        to_download.seek(0)
        st.download_button(
            label="📥 Download Full Prediction History",
            data=to_download,
            file_name="prediction_history.xlsx",
            mime="application/vnd.ms-excel"
        )
