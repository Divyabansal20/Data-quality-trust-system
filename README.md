# 🛡️ Data Trust Scoring System

A professional-grade Data Quality (DQ) audit tool built with Python and Streamlit. This system evaluates datasets across five key dimensions to determine "Analytical Readiness."

## 🚀 Live Demo

## ✨ Key Features
- **Multi-Dimensional Auditing:** Checks for Completeness, Validity, Accuracy, Consistency, and Uniqueness.
- **Statistical Accuracy:** Uses skewness-aware outlier detection (switching between Z-Score and IQR).
- **Smart Scoring Engine:** Implements a multiplicative penalty algorithm to realistically assess data health.
- **Automated Reporting:** Generates a professional PDF Audit Report for stakeholders.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Data Engine:** Pandas, NumPy, SciPy
- **Reporting:** FPDF

## 📊 Scoring Methodology
The system uses a weighted base score ($Base = \sum (Health_i \times Weight_i)$) combined with a 15% exponential decay penalty for every "Critical" failure found.