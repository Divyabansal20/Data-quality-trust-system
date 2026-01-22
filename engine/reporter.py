# from fpdf import FPDF
# import datetime

# def generate_risk_assessment(trust_score, comp, acc, consist):
#     # 1. Determine Risk Tier
#     if trust_score > 90:
#         risk_level = "LOW RISK"
#         verdict = "The dataset is structurally sound and safe for analytics."
#     elif trust_score > 70:
#         risk_level = "MODERATE RISK"
#         verdict = "Significant noise detected. Requires manual cleaning before use."
#     else:
#         risk_level = "HIGH RISK"
#         verdict = "Data is unreliable. Major structural or logic failures detected."

#     # 2. Generate Action Plan
#     actions = []
#     critical_comp = [c for c, m in comp.items() if m['status'] == 'Critical']
#     if critical_comp:
#         actions.append(f"DROP/FIX: Columns {', '.join(critical_comp)} have severe missingness.")
    
#     if any(i['status'] != 'Excellent' for i in consist if " -> " in i['rule']):
#         actions.append("AUDIT: Verify logic relationships to resolve pattern breaches.")

#     action_plan = " ".join(actions) if actions else "No immediate corrective actions required."
#     return risk_level, verdict, action_plan
# def generate_pdf(trust_score, comp, dupe, valid, acc, consist, profile, dataset_name):

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15) 
#     pdf.add_page()
    
#     # --- Title Section ---
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, "Data Trust Audit Report", 0, 1, "C")
    
#     # Date and Dataset Name
#     pdf.set_font("Arial", "", 10)
#     pdf.cell(0, 8, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
#     pdf.set_font("Arial", "I", 10)
#     pdf.cell(0, 8, f"Dataset: {dataset_name}", 0, 1, "C")
#     pdf.ln(5)

#     # --- Score (No Box) ---
#     pdf.set_font("Arial", "B", 24)
#     pdf.cell(0, 20, f"Overall Trust Score: {trust_score}%", 0, 1, "C")
#     pdf.ln(5)

#     # --- 1. Dataset Identity (No Box) ---
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 10, "1. Dataset Identity", 0, 1, 'L')
#     pdf.set_font("Arial", "", 10)
    
#     intro_text = (
#         f"This audit evaluates a dataset containing {profile['rows']} records and {profile['cols']} columns. "
#         f"The system identified {len(profile['numeric_cols'])} numeric features and "
#         f"{len(profile['text_cols'])} categorical features. Total size: {profile['file_size_kb']} KB."
#     )
#     pdf.multi_cell(0, 8, intro_text, 0) # Border set to 0
#     pdf.ln(5)

#     # --- 2. Executive Risk Assessment ---
#     risk_lvl, verdict, action_plan = generate_risk_assessment(trust_score, comp, acc, consist)
    
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 10, "2. Executive Risk Assessment", 0, 1)
    
#     pdf.set_font("Arial", "B", 11)
#     pdf.cell(30, 8, "STATUS:", 0, 0)
#     pdf.set_font("Arial", "", 11)
#     pdf.cell(0, 8, risk_lvl, 0, 1)
    
#     # pdf.set_font("Arial", "B", 11)
#     # pdf.cell(30, 8, "VERDICT:", 0, 0)
#     pdf.set_font("Arial", "", 11)
#     pdf.cell(0, 8, verdict, 0, 1)
    
#     # Action Plan (No Box)
#     pdf.ln(2)
#     pdf.set_font("Arial", "B", 10)
#     pdf.cell(0, 8, "Recommended Action Plan:", 0, 1)
#     pdf.set_font("Arial", "", 10)
#     pdf.multi_cell(0, 8, action_plan, 0) # Border set to 0
#     pdf.ln(10)

#     # --- Technical Tables (Kept with borders for tabular clarity) ---
    
#     # 3. Completeness
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 10, "3. Completeness Report", 0, 1)
#     pdf.set_font("Arial", "B", 10)
#     pdf.cell(60, 8, "Column Name", 1)
#     pdf.cell(60, 8, "Missing %", 1)
#     pdf.cell(60, 8, "Status", 1, 1) 
#     pdf.set_font("Arial", "", 10)
#     for col, metrics in comp.items():
#         pdf.cell(60, 8, str(col), 1)
#         pdf.cell(60, 8, f"{metrics['missing percentage']}%", 1)
#         pdf.cell(60, 8, metrics['status'], 1, 1)

#     # 4. Validity
#     pdf.ln(10)
#     pdf.set_font('Arial', 'B', 12)
#     pdf.cell(0, 10, "4. Validity Report", 0, 1, 'L')
#     pdf.set_font('Arial', 'B', 10)
#     pdf.cell(90, 8, "Column name", 1)
#     pdf.cell(90, 8, "Status", 1, 1)
#     pdf.set_font('Arial', '', 10)
#     for col, metrics in valid.items():
#         pdf.cell(90, 8, str(col), 1)
#         pdf.cell(90, 8, metrics['status'], 1, 1)

#     # 5. Accuracy
#     pdf.ln(10)
#     pdf.set_font('Arial', 'B', 12)
#     pdf.cell(0, 10, "5. Accuracy (Outlier Detection)", 0, 1, 'L')
#     pdf.set_font('Arial', 'B', 10)
#     pdf.cell(60, 8, "Column name", 1)
#     pdf.cell(60, 8, "Outliers Found", 1)
#     pdf.cell(60, 8, "Status", 1, 1)
#     pdf.set_font('Arial', '', 10)
#     for col, metrics in acc.items():
#         pdf.cell(60, 8, str(col), 1)
#         pdf.cell(60, 8, str(metrics['outlier_count']), 1)
#         pdf.cell(60, 8, metrics['status'], 1, 1)

#     # 6. Uniqueness (No Box)
#     pdf.ln(10)
#     pdf.set_font('Arial', 'B', 12)
#     pdf.cell(0, 10, "6. Uniqueness Report", 0, 1, 'L')
#     pdf.set_font('Arial', '', 10)
#     pdf.multi_cell(0, 8, f"Status: {dupe['status']}\nDuplicates Found: {dupe['duplicate count']} rows", 0)

#     # 7. Consistency (No Box)
#     pdf.ln(10)
#     pdf.set_font('Arial', 'B', 12)
#     pdf.cell(0, 10, "7. Consistency (Logical Integrity)", 0, 1, 'L')
#     for issue in consist:
#         if " -> " in issue['rule']:
#             rule_parts = issue['rule'].split(" -> ")
#             display_rule = f"RULE: Values in '{rule_parts[0]}' must uniquely determine values in '{rule_parts[1]}'."
#         else:
#             display_rule = f"RULE: {issue['rule']}"
        
#         pdf.set_font('Arial', 'B', 10)
#         pdf.multi_cell(0, 8, display_rule, 0, 'L')
#         pdf.set_font('Arial', '', 10)
#         pdf.multi_cell(0, 8, f"OBSERVATION: {issue['issue']} | Status: {issue['status']}", 0, 'L')
#         pdf.ln(2)

#     # --- Footer ---
#     pdf.ln(10)
#     pdf.set_font("Arial", "I", 8)
#     pdf.cell(0, 10, "End of Audit Report. Generated by Local Heuristic Engine.", 0, 0, "C")

#     return pdf.output(dest='S').encode('latin-1')



from fpdf import FPDF
import datetime

def generate_risk_assessment(trust_score, comp, valid, acc, consist):
    """Holistic risk assessment based on all DQ dimensions."""
    # 1. Determine Risk Tier
    if trust_score >= 90:
        risk_level = "LOW RISK"
        verdict = "The dataset is structurally sound and safe for production analytics."
    elif trust_score >= 70:
        risk_level = "MODERATE RISK"
        verdict = "Significant noise or inconsistencies detected. Review before use."
    else:
        risk_level = "HIGH RISK"
        verdict = "Data is unreliable. Significant structural or integrity failures found."

    # 2. Generate Multi-Dimensional Action Plan
    actions = []
    
    # Check Completeness & Validity
    crit_cols = [c for c, m in comp.items() if m['status'] == 'Critical']
    invalid_cols = [c for c, m in valid.items() if m['status'] == 'Critical']
    
    if crit_cols:
        actions.append(f"FIX: High missingness in {', '.join(crit_cols)}.")
    if invalid_cols:
        actions.append(f"REFORMAT: Type mismatches detected in {', '.join(invalid_cols)}.")
    
    # Check Outliers
    high_outliers = [c for c, m in acc.items() if m['status'] == 'Critical']
    if high_outliers:
        actions.append(f"SCRUB: Excessive outliers in {', '.join(high_outliers)} may bias analysis.")

    # Check Consistency
    if any(i['status'] != 'Excellent' for i in consist if "rule" in i):
        actions.append("RESOLVE: Logical pattern breaches found in Consistency report.")

    action_plan = " | ".join(actions) if actions else "No immediate corrective actions required."
    return risk_level, verdict, action_plan

def generate_pdf(trust_score, comp, dupe, valid, acc, consist, profile, dataset_name):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15) 
    pdf.add_page()
    
    # --- Header ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Data Trust Audit Report", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')} | Dataset: {dataset_name}", 0, 1, "C")
    pdf.ln(5)

    # --- Score Section ---
    pdf.set_font("Arial", "B", 26)
    pdf.cell(0, 20, f"Overall Trust Score: {trust_score}%", 0, 1, "C")
    pdf.ln(5)

    # --- 1. Dataset Identity ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Dataset Identity", 0, 1)
    pdf.set_font("Arial", "", 10)
    intro_text = (f"Records: {profile['rows']} | Columns: {profile['cols']} | "
                  f"Numeric: {len(profile['numeric_cols'])} | Categorical: {len(profile['text_cols'])} | "
                  f"Size: {profile['file_size_kb']} KB")
    pdf.cell(0, 8, intro_text, 0, 1)

    # --- 2. Executive Assessment ---
    risk_lvl, verdict, action_plan = generate_risk_assessment(trust_score, comp, valid, acc, consist)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Executive Risk Assessment", 0, 1)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(30, 8, "STATUS:", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, risk_lvl, 0, 1)
    pdf.multi_cell(0, 8, f"VERDICT: {verdict}", 0)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "Recommended Action Plan:", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, action_plan, 0)

    # --- Technical Reports (Detailed Tables) ---
    # 3. Completeness & Validity (Merged for space)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Format & Completeness Audit", 0, 1)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(50, 8, "Column", 1); pdf.cell(40, 8, "Type", 1); pdf.cell(30, 8, "Missing %", 1); pdf.cell(30, 8, "Valid %", 1); pdf.cell(35, 8, "Status", 1, 1)
    pdf.set_font("Arial", "", 9)
    for col in comp.keys():
        pdf.cell(50, 8, str(col)[:20], 1)
        pdf.cell(40, 8, valid[col]['inferred_type'], 1) # Display Smart Type
        pdf.cell(30, 8, f"{comp[col]['missing percentage']}%", 1)
        pdf.cell(30, 8, f"{valid[col]['valid_ratio']}", 1)
        pdf.cell(35, 8, comp[col]['status'], 1, 1)

    # 4. Accuracy (Outliers)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "4. Accuracy (Statistical Outliers)", 0, 1)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(60, 8, "Column", 1); pdf.cell(40, 8, "Method", 1); pdf.cell(40, 8, "Outliers", 1); pdf.cell(40, 8, "Status", 1, 1)
    pdf.set_font('Arial', '', 9)
    for col, m in acc.items():
        pdf.cell(60, 8, str(col)[:25], 1)
        pdf.cell(40, 8, m['method_used'], 1) # Display Z-Score/IQR
        pdf.cell(40, 8, str(m['outlier_count']), 1)
        pdf.cell(40, 8, m['status'], 1, 1)

    # 5. Consistency & Uniqueness Summary
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "5. Integrity & Uniqueness Summary", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, f"Duplicates found: {dupe['duplicate count']} ({dupe['duplicate percentage']}%). Status: {dupe['status']}", 0)
    for issue in consist:
        if issue['status'] != "Excellent":
            pdf.multi_cell(0, 7, f"LOGIC BREACH: {issue['rule']} | {issue['issue']}", 0)

    # --- Footer ---
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Report generated by Weighted Trust Scoring Engine v2.0", 0, 0, "C")

    return pdf.output(dest='S').encode('latin-1')