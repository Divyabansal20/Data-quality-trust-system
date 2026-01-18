from fpdf import FPDF
import datetime

def generate_pdf(trust_score, comp, dupe, valid, acc, consist):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15) 
    pdf.add_page()
    
    #Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Data Trust Audit Report", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
    pdf.ln(10)

    #Score Box
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, f"Overall Trust Score: {trust_score}%", 1, 1, "C")
    pdf.ln(10)

    # Completeness Report
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Completeness Report", 0, 1)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 8, "Column Name", 1)
    pdf.cell(60, 8, "Missing %", 1)
    pdf.cell(60, 8, "Status", 1, 1) 

    pdf.set_font("Arial", "", 10)
    for col, metrics in comp.items():
        pdf.cell(60, 8, str(col), 1)
        pdf.cell(60, 8, f"{metrics['missing percentage']}%", 1)
        pdf.cell(60, 8, metrics['status'], 1, 1)

    # Validity Report
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "2. Validity Report", 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(90, 8, "Column name", 1)
    pdf.cell(90, 8, "Status", 1, 1)
    
    pdf.set_font('Arial', '', 10)
    for col, metrics in valid.items():
        pdf.cell(90, 8, str(col), 1)
        pdf.cell(90, 8, metrics['status'], 1, 1)

    # Accuracy Report
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "3. Accuracy Report (Outlier Detection)", 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 8, "Column name", 1)
    pdf.cell(60, 8, "Outliers Found", 1)
    pdf.cell(60, 8, "Status", 1, 1)
    
    pdf.set_font('Arial', '', 10)
    for col, metrics in acc.items():
        pdf.cell(60, 8, str(col), 1)
        pdf.cell(60, 8, str(metrics['outlier_count']), 1)
        pdf.cell(60, 8, metrics['status'], 1, 1)

    # Uniqueness Report
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "4. Uniqueness Report", 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 8, f"Status: {dupe['status']}\nDuplicates Found: {dupe['duplicate count']} rows", 1)

    # Consistency Report 
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "5. Consistency Report (Logical Integrity)", 0, 1, 'L')
    
    for issue in consist:
        rule_parts = issue['rule'].split(" -> ")
        col_a, col_b = rule_parts[0], rule_parts[1]
        
        # Rule Box
        pdf.set_font('Arial', 'B', 10)
        pdf.multi_cell(0, 8, f"RULE: Values in '{col_a}' must uniquely determine values in '{col_b}'.", 1, 'L', fill=False)
        
        # Observation Box
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 8, f"OBSERVATION: Found {issue['issue']} Status: {issue['status']}", 1, 'L')
        
        pdf.ln(4)
    return pdf.output(dest='S').encode('latin-1')