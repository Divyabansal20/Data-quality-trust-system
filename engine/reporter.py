from fpdf import FPDF
import datetime

def generate_pdf(trust_score, comp, dupe, valid, acc, consist):
    # 1. Setup the 'Paper'
    pdf = FPDF()
    # This line ensures that if a table is too long, it continues on page 2
    pdf.set_auto_page_break(auto=True, margin=15) 
    pdf.add_page()
    
    # 2. Add a Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Data Trust Audit Report", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
    pdf.ln(10)

    # 3. Big Score Box
    # We use '1' for the border to make it look like a certificate
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, f"Overall Trust Score: {trust_score}%", 1, 1, "C")
    pdf.ln(10)

    # --- 1. Completeness Report ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Completeness Report", 0, 1)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 8, "Column", 1)
    pdf.cell(60, 8, "Missing %", 1)
    pdf.cell(60, 8, "Status", 1, 1) # ln=1 moves cursor to the next line

    pdf.set_font("Arial", "", 10)
    for col, metrics in comp.items():
        pdf.cell(60, 8, str(col), 1)
        pdf.cell(60, 8, f"{metrics['missing percentage']}%", 1)
        pdf.cell(60, 8, metrics['status'], 1, 1)

    # --- 2. Validity Report ---
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "2. Validity Report (Numeric Ratios)", 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(90, 8, "Column", 1)
    pdf.cell(90, 8, "Status", 1, 1)
    
    pdf.set_font('Arial', '', 10)
    for col, metrics in valid.items():
        pdf.cell(90, 8, str(col), 1)
        pdf.cell(90, 8, metrics['status'], 1, 1)

    # --- 3. Accuracy Report (Outliers) ---
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "3. Accuracy Report (Outlier Detection)", 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 8, "Column", 1)
    pdf.cell(60, 8, "Outliers Found", 1)
    pdf.cell(60, 8, "Status", 1, 1)
    
    pdf.set_font('Arial', '', 10)
    # Titanic has numeric and non-numeric; acc only contains numeric
    for col, metrics in acc.items():
        pdf.cell(60, 8, str(col), 1)
        pdf.cell(60, 8, str(metrics['outlier_count']), 1)
        pdf.cell(60, 8, metrics['status'], 1, 1)

    # --- 4. Uniqueness Report ---
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "4. Uniqueness Report", 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 8, f"Status: {dupe['status']}\nDuplicates Found: {dupe['duplicate count']} rows", 1)

    # --- 5. Consistency Report ---
    # We add a page break if we are near the bottom to keep the report clean
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "5. Consistency Report (Pattern Breaches)", 0, 1, 'L')
    
    pdf.set_font('Arial', '', 10)
    for issue in consist:
        # multi_cell is critical here because Titanic consistency 
        # issues like 'Ticket -> Cabin' can be long.
        pdf.multi_cell(0, 8, f"- {issue['rule']}: {issue['issue']} ({issue['status']})", 1)

    # 5. Turn the 'Paper' into data for the Streamlit button
    # dest='S' returns the PDF as a byte string
    return pdf.output(dest='S').encode('latin-1')