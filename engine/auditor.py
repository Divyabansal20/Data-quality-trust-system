import pandas as pd

def completeness_check(df):
    completeness_results={}
    
    missing_vals= df.isnull().sum()
    total_rows= len(df)

    for column in df.columns:
        count= int(missing_vals[column])
        percentage= (count/total_rows)*100

        if percentage==0:
            status="Excellent"
        elif percentage<5:
            status="Good"
        elif percentage<20:
            status="Warning"
        else:
            status="Critical"
        completeness_results[column]={
            "missing values": count,
            "missing percentage":round(percentage,2),
            "status":status
        }
    return completeness_results

def duplicate_check(df):
    # duplicate_results={}
    total_duplicates= int(df.duplicated().sum())
    total_rows= len(df)
    dup_perc= (total_duplicates/total_rows)*100

    if dup_perc==0:
        status="Excellent"
    elif  dup_perc<5:
        status="Warning"
    else:
        status="Critical"
    return {
        "duplicate count":total_duplicates,
        "duplicate percentage": dup_perc,
        "status": status
    }
