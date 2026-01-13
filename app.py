import streamlit as st
from engine.auditor import completeness_check, duplicate_check
from engine.scorer import calculate_trust_score
from utils.loader import load_dataset

st.title("Data Trust Scoring System")
st.write("Upload a dataset to evaluate its analytical readiness")
uploaded_file= st.file_uploader("Choose a CSV or Excel file",type=['csv','xlsx'])

if uploaded_file is not None:
    df,error= load_dataset(uploaded_file)

    if error:
        st.error(f"Error loading the file: {error}")
    else:
        st.success("File loaded successfully!")
        
    
    completeness_result= completeness_check(df)
    duplicates_Result= duplicate_check(df)
    trustScore= calculate_trust_score(completeness_result,duplicates_Result)
    st.metric(label="Overall Trust Score",value=f"{trustScore}%")
    st.subheader("🛠️ Auditor Diagnostics")
    st.write(completeness_result)
    st.write(duplicates_Result)