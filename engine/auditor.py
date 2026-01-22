import pandas as pd
import numpy as np
from scipy.stats import skew

def get_dataset_profile(df):
    """Gathers metadata to provide context in the report."""
    if df.empty:
        return {"rows": 0, "cols": 0, "numeric_cols": [], "text_cols": [], "file_size_kb": 0}
    
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "numeric_cols": list(df.select_dtypes(include=['number']).columns),
        "text_cols": list(df.select_dtypes(exclude=['number']).columns),
        "file_size_kb": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }

# --- HELPER FUNCTIONS ---

def infer_column_type(series):
    """Determines if a column is Numeric, Temporal, or Categorical."""
    if series.empty:
        return "Empty"
    
    # 1. Check if it's already numeric
    if pd.api.types.is_numeric_dtype(series):
        return "Numeric"
    
    # 2. Try to convert to datetime (with a length check to avoid misidentifying IDs)
    sample = series.dropna().head(100).astype(str)
    if sample.str.len().mean() > 4:
        try:
            pd.to_datetime(sample, errors='raise')
            return "Temporal"
        except:
            pass
    
    # 3. Check if it's categorical (low cardinality: unique values < 5% of total)
    if series.nunique() / len(series) < 0.05:
        return "Categorical"
    
    return "Text/Other"

def get_outlier_method(series):
    """Decides whether to use Z-Score or IQR based on skewness."""
    data = series.dropna()
    if len(data) < 3: 
        return "None"
    
    s = skew(data)
    # If skew is between -0.5 and 0.5, it's roughly symmetric (Gaussian)
    if -0.5 < s < 0.5:
        return "Z-Score"
    else:
        return "IQR"

# --- CORE CHECKS ---

def completeness_check(df):
    completeness_results = {}
    missing_vals = df.isnull().sum()
    total_rows = len(df)

    for column in df.columns:
        count = int(missing_vals[column])
        percentage = (count / total_rows) * 100 if total_rows > 0 else 0
        
        if percentage == 0:
            status = "Excellent"
        elif percentage < 20:
            status = "Warning"
        else:
            status = "Critical"
            
        completeness_results[column] = {
            "missing values": count,
            "missing percentage": round(percentage, 2),
            "status": status
        }
    return completeness_results

def duplicate_check(df):
    if df.empty:
        return {"duplicate count": 0, "duplicate percentage": 0, "status": "Excellent"}
        
    total_duplicates = int(df.duplicated().sum())
    total_rows = len(df)
    dup_perc = (total_duplicates / total_rows) * 100

    if dup_perc == 0:
        status = "Excellent"
    elif dup_perc < 5:
        status = "Warning"
    else:
        status = "Critical"
        
    return {
        "duplicate count": total_duplicates,
        "duplicate percentage": round(dup_perc, 2),
        "status": status
    }

def validity_check(df):
    validity_results = {}
    for col in df.columns:
        col_type = infer_column_type(df[col])
        total_vals = len(df[col])
        
        if total_vals == 0:
            valid_ratio = 0
        elif col_type == "Numeric":
            valid_count = pd.to_numeric(df[col], errors='coerce').notnull().sum()
            valid_ratio = valid_count / total_vals
        elif col_type == "Temporal":
            valid_count = pd.to_datetime(df[col], errors='coerce').notnull().sum()
            valid_ratio = valid_count / total_vals
        else:
            # For Categorical,t non-null is valid
            valid_ratio = df[col].notnull().sum() / total_vals

        if valid_ratio >= 0.98:
            status = "Excellent"
        elif valid_ratio >= 0.90:
            status = "Warning"
        else:
            status = "Critical"

        validity_results[col] = {
            "inferred_type": col_type,
            "valid_ratio": f"{round(valid_ratio * 100, 2)}%",
            "status": status
        }
    return validity_results

def audit_accuracy(df):
    accuracy_results = {}
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty: continue
        
        method = get_outlier_method(series)
        outlier_count = 0
        lower_limit, upper_limit = 0, 0
        
        if method == "Z-Score":
            mean, std = series.mean(), series.std()
            lower_limit, upper_limit = mean - 3 * std, mean + 3 * std
            outliers = series[(series < lower_limit) | (series > upper_limit)]
        elif method == "IQR":
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower_limit, upper_limit = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = series[(series < lower_limit) | (series > upper_limit)]
        else:
            outlier_count = 0
            outliers = []

        outlier_count = len(outliers)
        status = "Excellent"
        if outlier_count > 0:
            status = "Warning"
        if outlier_count > (0.05 * len(df)): 
            status = "Critical"

        accuracy_results[col] = {
            "method_used": method,
            "outlier_count": outlier_count,
            "lower_limit": round(lower_limit, 2),
            "upper_limit": round(upper_limit, 2),
            "status": status
        }
    return accuracy_results

def audit_consistency(df):
    consistency_results = []
    cols = df.columns
    
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            col_a, col_b = cols[i], cols[j]
            # Check if col_a could be a potential Key
            if df[col_a].nunique() / len(df) > 0.5:
                mismatches = df.groupby(col_a)[col_b].nunique()
                violations = mismatches[mismatches > 1]
                
                if not violations.empty:
                    violation_ratio = len(violations) / df[col_a].nunique()
                    status = "Critical" if violation_ratio > 0.1 else "Warning"
            
                    consistency_results.append({
                        "rule": f"{col_a} -> {col_b}",
                        "issue": f"{len(violations)} groups in '{col_a}' have conflicting values in '{col_b}'.",
                        "status": status
                    })
    
    if not consistency_results:
        consistency_results.append({"rule": "Logical Integrity", "issue": "No pattern breaches found.", "status": "Excellent"})
    return consistency_results


def calculate_final_trust_score(completeness, uniqueness, validity, accuracy):
    """Calculates a weighted trust score based on four key DQ dimensions."""
    weights = {
        'completeness': 0.35, 
        'validity': 0.30,      
        'uniqueness': 0.15,    
        'accuracy': 0.20       
    }

    status_map = {"Excellent": 1.0, "Warning": 0.7, "Critical": 0.4}

    def get_dim_score(results_dict):
        if not results_dict: return 1.0
        scores = [status_map.get(v['status'], 0) for v in results_dict.values()]
        return sum(scores) / len(scores)

    u_score = status_map.get(uniqueness['status'], 0)
    
    dim_scores = {
        'completeness': get_dim_score(completeness),
        'validity': get_dim_score(validity),
        'uniqueness': u_score,
        'accuracy': get_dim_score(accuracy)
    }

    final_score = sum(dim_scores[dim] * weights[dim] for dim in weights)
    return round(final_score * 100, 2), dim_scores









# import pandas as pd
# import numpy as np


# def get_dataset_profile(df):
#     """Gathers metadata to provide context in the report."""
#     return {
#         "rows": len(df),
#         "cols": len(df.columns),
#         "numeric_cols": list(df.select_dtypes(include=['number']).columns),
#         "text_cols": list(df.select_dtypes(exclude=['number']).columns),
#         "file_size_kb": round(df.memory_usage(deep=True).sum() / 1024, 2)
#     }


# # 1. completeness check
# def completeness_check(df):
#     completeness_results={}
    
#     missing_vals= df.isnull().sum()
#     total_rows= len(df)

#     for column in df.columns:
#         count= int(missing_vals[column])
#         percentage= (count/total_rows)*100
#         if percentage==0:
#             status="Excellent"
#         elif percentage<20:
#             status="Warning"
#         else:
#             status="Critical"
#         completeness_results[column]={
#             "missing values": count,
#             "missing percentage":round(percentage,2),
#             "status":status
#         }
#     return completeness_results

# # 2. Duplicates check


# def duplicate_check(df):
#     total_duplicates= int(df.duplicated().sum())
#     total_rows= len(df)
#     dup_perc= (total_duplicates/total_rows)*100

#     if dup_perc==0:
#         status="Excellent"
#     elif  dup_perc<5:
#         status="Warning"
#     else:
#         status="Critical"
#     return {
#         "duplicate count":total_duplicates,
#         "duplicate percentage": dup_perc,
#         "status": status
#     }

# # 3. Validity check


# # def validity_check(df):
# #     validity_results={}
# #     for col in df.columns:
# #         total_vals=len(df[col])
# #         numeric_count= pd.to_numeric(df[col],errors="coerce").notnull().sum()

# #         numeric_ratio= numeric_count/total_vals
# #         status= "Excellent"
# #         if(0.7< numeric_ratio<1):
# #             status="Critical"
# #         elif 0.0<=numeric_ratio <=0.7:
# #             status="Warning"
# #         validity_results[col]={
# #             "numeric ratio": f"{round(numeric_ratio*100,2)}%" ,
# #             "status": status
# #         }
# #     return validity_results




# def infer_column_type(series):
#     """Determines if a column is Numeric, Temporal, or Categorical."""
#     # 1. Check if it's already numeric
#     if pd.api.types.is_numeric_dtype(series):
#         return "Numeric"
    
#     # 2. Try to convert to datetime
#     # We use a sample to speed it up for large datasets
#     sample = series.dropna().head(100)
#     try:
#         pd.to_datetime(sample, errors='raise')
#         return "Temporal"
#     except:
#         pass
    
#     # 3. Check if it's categorical (low cardinality)
#     if series.nunique() / len(series) < 0.05:
#         return "Categorical"
    
#     return "Text/Other"



# def validity_check(df):
#     validity_results = {}
#     for col in df.columns:
#         col_type = infer_column_type(df[col])
#         total_vals = len(df[col])
        
#         if col_type == "Numeric":
#             # For numeric, validity is high if few non-numeric strings exist
#             valid_count = pd.to_numeric(df[col], errors='coerce').notnull().sum()
#         elif col_type == "Temporal":
#             # For dates, validity is high if they actually parse as dates
#             valid_count = pd.to_datetime(df[col], errors='coerce').notnull().sum()
#         else:
#             # For categories/text, validity is usually based on completeness
#             valid_count = df[col].notnull().sum()

#         validity_ratio = valid_count / total_vals
        
#         # Professional Scoring Logic
#         if validity_ratio >= 0.98:
#             status = "Excellent"
#         elif validity_ratio >= 0.90:
#             status = "Warning"
#         else:
#             status = "Critical"

#         validity_results[col] = {
#             "inferred_type": col_type,
#             "valid_ratio": f"{round(validity_ratio * 100, 2)}%",
#             "status": status
#         }
#     return validity_results


# # 4. Accuracy check


# from scipy.stats import skew

# def get_outlier_method(series):
#     """Decides whether to use Z-Score or IQR based on skewness."""
#     # Remove nulls for calculation
#     data = series.dropna()
#     if len(data) < 3: return "None"
    
#     # Calculate skewness
#     s = skew(data)
    
#     # Threshold: If skew is between -0.5 and 0.5, it's roughly symmetric
#     if -0.5 < s < 0.5:
#         return "Z-Score"
#     else:
#         return "IQR"

# def audit_accuracy(df):
#     accuracy_results = {}
#     numeric_cols = df.select_dtypes(include=['number']).columns
    
#     for col in numeric_cols:
#         series = df[col].dropna()
#         if series.empty: continue
        
#         method = get_outlier_method(series)
#         outlier_count = 0
#         lower_limit, upper_limit = 0, 0
        
#         if method == "Z-Score":
#             mean = series.mean()
#             std = series.std()
#             lower_limit = mean - 3 * std
#             upper_limit = mean + 3 * std
#             outliers = series[(series < lower_limit) | (series > upper_limit)]
#         else: # IQR Method
#             q1 = series.quantile(0.25)
#             q3 = series.quantile(0.75)
#             iqr = q3 - q1
#             lower_limit = q1 - 1.5 * iqr
#             upper_limit = q3 + 1.5 * iqr
#             outliers = series[(series < lower_limit) | (series > upper_limit)]
            
#         outlier_count = len(outliers)
        
#         # Professional Scoring Logic
#         status = "Excellent"
#         if outlier_count > 0:
#             status = "Warning"
#         if outlier_count > (0.05 * len(df)): # Lowered threshold to 5% for professional standards
#             status = "Critical"

#         accuracy_results[col] = {
#             "method_used": method,
#             "outlier_count": outlier_count,
#             "lower_limit": round(lower_limit, 2),
#             "upper_limit": round(upper_limit, 2),
#             "status": status
#         }
#     return accuracy_results

# # 5. Consistency check


# def audit_consistency(df):
#     consistency_results = []
#     cols = df.columns
    
#     for i in range(len(cols)):
#         for j in range(i + 1, len(cols)):
#             col_a, col_b = cols[i], cols[j]
#             a_uniqueness = df[col_a].nunique() / len(df)
            
#             if a_uniqueness > 0.5:
#                 mismatches = df.groupby(col_a)[col_b].nunique()
#                 violations = mismatches[mismatches > 1]
                
#                 if not violations.empty:
#                     violation_ratio = len(violations) / df[col_a].nunique()
            
#                     status = "Critical" if violation_ratio > 0.1 else "Warning"
            
#                     consistency_results.append({
#                         "rule": f"{col_a} -> {col_b}",
#                         "issue": f"{len(violations)} groups in '{col_a}' have conflicting values in '{col_b}'.",
#                         "status": status
#                     })
    
#     if not consistency_results:
#         consistency_results.append({"rule": "Logical Integrity", "issue": "No pattern breaches found.", "status": "Excellent"})
        
#     return consistency_results

# def calculate_final_trust_score(completeness, uniqueness, validity, accuracy):
#     """
#     Calculates a weighted trust score based on four key DQ dimensions.
#     Weights are adjustable based on industry standards.
#     """
#     # Define Weights (Total = 1.0)
#     weights = {
#         'completeness': 0.35,  # Missing data is the biggest risk
#         'validity': 0.30,      # Wrong formats break pipelines
#         'uniqueness': 0.15,    # Duplicates are bad but often fixable
#         'accuracy': 0.20       # Outliers might be real domain events
#     }

#     # Helper to convert "Status" to a numeric score
#     status_map = {"Excellent": 1.0, "Warning": 0.7, "Critical": 0.4}

#     # 1. Dimension Scores (averaging statuses across columns)
#     def get_dim_score(results_dict):
#         if not results_dict: return 1.0
#         # If it's a list (Consistency check), handle differently, 
#         # but for these four, they are dictionaries.
#         scores = [status_map.get(v['status'], 0) for v in results_dict.values()]
#         return sum(scores) / len(scores)

#     # Note: Uniqueness is a single dict in your code, not per-column
#     u_score = status_map.get(uniqueness['status'], 0)
    
#     dim_scores = {
#         'completeness': get_dim_score(completeness),
#         'validity': get_dim_score(validity),
#         'uniqueness': u_score,
#         'accuracy': get_dim_score(accuracy)
#     }

#     # 2. Final Weighted Calculation
#     final_score = sum(dim_scores[dim] * weights[dim] for dim in weights)
    
#     return round(final_score * 100, 2), dim_scores