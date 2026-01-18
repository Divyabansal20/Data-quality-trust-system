import streamlit as st
import pandas as pd
from engine.auditor import completeness_check, duplicate_check, validity_check, audit_accuracy, audit_consistency
from engine.scorer import calculate_trust_score
from utils.loader import load_dataset
from engine.reporter import generate_pdf


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
    accuracy_results= audit_accuracy(df)
    consistency_results= audit_consistency(df)
    trustScore= calculate_trust_score(completeness_result,duplicates_Result,validity_results, accuracy_results, consistency_results)

    st.divider()
    st.metric(label="Overall Trust Score",value=f"{trustScore}%")

    
    pdf_bytes = generate_pdf(trustScore, completeness_result, duplicates_Result, 
                            validity_results, accuracy_results, consistency_results)

    st.download_button(
        label="Download Audit Report",
        data=pdf_bytes,
        file_name="Data_Trust_Report.pdf",
        mime="application/pdf"
    )

    col1, col2= st.columns(2)
    with col1:
        st.subheader("Completeness Check")
        completeness_df= pd.DataFrame(completeness_result).T
        st.dataframe(completeness_df, use_container_width=True)
    with col2:
        st.subheader("Uniqueness Check")
        st.write(f"Duplicate status: **{duplicates_Result['status']}**")
        st.write(f"Duplicates found: {duplicates_Result['duplicate count']}")
        
    col1, col2= st.columns(2)
    with col1:
        st.subheader("Validity Check")
        validity_df= pd.DataFrame(validity_results).T
        st.dataframe(validity_df, use_container_width=True)    
    with col2:
        st.subheader("Accuracy Check")
        accuracy_df= pd.DataFrame(accuracy_results).T
        st.dataframe(accuracy_df, use_container_width=True)  
    
    st.subheader("Consistency Check")
    consistency_df= pd.DataFrame(consistency_results)
    st.dataframe(consistency_df, use_container_width=True)


