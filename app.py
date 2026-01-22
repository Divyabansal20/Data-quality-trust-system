import streamlit as st
import pandas as pd
import numpy as np
from engine.auditor import (
    completeness_check, 
    duplicate_check, 
    validity_check, 
    audit_accuracy, 
    audit_consistency, 
    get_dataset_profile
)
from engine.scorer import calculate_trust_score
from utils.loader import load_dataset
from engine.reporter import generate_pdf

st.set_page_config(
    page_title="Data Trust Scoring System",
    layout="wide"
)

st.title("Data Trust Scoring System")
st.markdown("""
Evaluate the **analytical readiness** of your datasets using a weighted scoring engine. 
This tool audits dimensions including Completeness, Validity, Accuracy, Consistency, and Uniqueness.
""")

with st.sidebar:
    st.header("Scoring Methodology")
    st.info("""
    **Weights:**
    - Completeness: 25%
    - Validity: 25%
    - Consistency: 20%
    - Accuracy: 15%
    - Uniqueness: 15%
    """)
    st.write("---")
    st.write("**Risk Tiers:**")
    st.success("90-100: Low Risk")
    st.warning("70-89: Medium Risk")
    st.error("<70: High Risk")

uploaded_file = st.file_uploader("Upload a CSV or Excel file (Max 200MB)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df, error = load_dataset(uploaded_file)
    
    if error:
        st.error(f"Error loading the file: {error}")
    else:
        with st.spinner('Performing Multi-Dimensional Quality Audit...'):
            dataset_profile = get_dataset_profile(df)
            comp_res = completeness_check(df)
            dupe_res = duplicate_check(df)
            val_res = validity_check(df)
            acc_res = audit_accuracy(df)
            cons_res = audit_consistency(df)
            
            trustScore = calculate_trust_score(
                comp_res, dupe_res, val_res, acc_res, cons_res
            )

        st.divider()
        m1, m2, m3 = st.columns([1, 1, 2])
        
        with m1:
            st.metric(label="Overall Trust Score", value=f"{trustScore}%")
            
        with m2:
            if trustScore >= 90:
                st.success("STATUS: LOW RISK")
                action_text = "Safe for production pipelines and ML modeling."
            elif trustScore >= 70:
                st.warning("STATUS: MEDIUM RISK")
                action_text = "Requires minor cleaning (outliers/missing data) before use."
            else:
                st.error("STATUS: HIGH RISK")
                action_text = "Unreliable for analytics. Requires significant manual audit."
        
        with m3:
            st.write(f"**Dataset Identity:** {uploaded_file.name}")
            st.write(f"**Shape:** {dataset_profile['rows']} rows × {dataset_profile['cols']} columns")
            st.caption(action_text)

        pdf_bytes = generate_pdf(
            trustScore, comp_res, dupe_res, val_res, 
            acc_res, cons_res, dataset_profile, uploaded_file.name
        )

        st.download_button(
            label="Download Professional Audit Report (PDF)",
            data=pdf_bytes,
            file_name=f"DQ_Report_{uploaded_file.name.split('.')[0]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.divider()
        st.subheader("Technical Drill-Down")
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Completeness", "Validity", "Accuracy", "Uniqueness", "Consistency"
        ])

        with tab1:
            st.write("Percentage of non-null values per column.")
            st.dataframe(pd.DataFrame(comp_res).T, use_container_width=True)

        with tab2:
            st.write("Data Type Integrity check against inferred business logic.")
            st.dataframe(pd.DataFrame(val_res).T, use_container_width=True)

        with tab3:
            st.write("Outlier detection using Skewness-aware Z-Score or IQR methods.")
            st.dataframe(pd.DataFrame(acc_res).T, use_container_width=True)

        with tab4:
            st.write("Identifying row-level redundancy.")
            st.info(f"Duplicate Row Status: **{dupe_res['status']}**")
            st.write(f"Total Duplicates: {dupe_res['duplicate count']} ({dupe_res['duplicate percentage']}%)")
            st.progress(max(0.0, 1.0 - (dupe_res['duplicate percentage'] / 100)))

        with tab5:
            st.write("Pattern breach detection (Logical Integrity).")
            st.dataframe(pd.DataFrame(cons_res), use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to begin the audit.")