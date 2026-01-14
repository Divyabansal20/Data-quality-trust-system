import pandas as pd
import numpy as np

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


def validity_check(df):
    validity_results={}
    for col in df.columns:
        total_vals=len(df[col])
        numeric_count= pd.to_numeric(df[col],errors="coerce").notnull().sum()

        numeric_ratio= numeric_count/total_vals
        status= "Excellent"
        if(0.7< numeric_ratio<1):
            status="Critical"
        elif 0.0<=numeric_ratio <=0.7:
            status="Warning"
        validity_results[col]={
            "numeric ratio": f"{round(numeric_ratio*100,2)}%" ,
            "status": status
        }
    return validity_results


def audit_accuracy(df):
    accuracy_results={}
    numeric_Cols= df.select_dtypes(include=['number']).columns
    for col in numeric_Cols:
        q1= df[col].quantile(0.25)
        q3= df[col].quantile(0.75)

        iqr= q3-q1

        lower_bound= q1- 1.5*iqr
        upper_bound= q3+ 1.5*iqr

        outliers= df[(df[col]<lower_bound)| (df[col]>upper_bound)]
        outlier_len= int(len(outliers))

        status= "Excellent"
        if outlier_len>0:
            status="Warning"
        if outlier_len > (0.1 * len(df)): 
            status = "Critical"

        accuracy_results[col] = {
            "outlier_count": outlier_len,
            "lower_limit": round(lower_bound, 2),
            "upper_limit": round(upper_bound, 2),
            "status": status
        }
    return accuracy_results