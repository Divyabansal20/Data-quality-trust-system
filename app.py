import streamlit as st
import pandas as pd
from engine.auditor import completeness_check, duplicate_check, validity_check
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
    validity_results = validity_check(df)
    trustScore= calculate_trust_score(completeness_result,duplicates_Result,validity_results)

    st.divider()
    st.metric(label="Overall Trust Score",value=f"{trustScore}%")

    col1, col2= st.columns(2)
    with col1:
        st.subheader("Completeness")
        completeness_df= pd.DataFrame(completeness_result).T
        st.dataframe(completeness_df, use_container_width=True)
    with col2:
        st.subheader("Uniqueness")
        st.write(f"Duplicate status: **{duplicates_Result['status']}**")
        st.write(f"Duplicates found: {duplicates_Result['duplicate count']}")
        
    st.divider()
    st.subheader("📍 Validity Report")
    validity_df = pd.DataFrame(validity_results).T
    st.dataframe(validity_df, use_container_width=True)