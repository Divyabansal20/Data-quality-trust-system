import pandas as pd

def completeness_check(df):
    audit_results={}
    
    missing_vals= df.isnull().sum()
    total_rows= len(df)

    for column in df.columns:
        count= missing_vals[column]
        percentage= (count/total_rows)*100

        if percentage==0:
            status="Excellent"
        elif percentage<5:
            status="Good"
        elif percentage<20:
            status="Warning"
        else:
            status="Critical"
        audit_results[column]={
            "missing columns": count,
            "missing percentage":round(percentage,2),
            "status":status
        }
        return audit_results