
def calculate_trust_score(completeness_results,duplicate_results,validity_results, accuracy_results,consistency_results):

    if not completeness_results:
        return 0
    
    penalty= {'Excellen':0,
              'Warning':5,
              'Critical':10
              }
    weights = {
        "comp": 0.25,  
        "valid": 0.25,   
        "consist": 0.20, 
        "acc": 0.15,     
        "dupe": 0.15     
    }
    
    # completeness
    completeness_penalty=0
    for cols, metric in completeness_results.items():
        completeness_penalty+=penalty.get(metric['status'],0)
    comp_health= 100- (completeness_penalty / len(completeness_results))

    # validity 
    valid_penalty=0
    for col, metrics in validity_results.items():
        valid_penalty += penalty.get(metrics["status"], 0)
    valid_health = 100 - (valid_penalty / len(validity_results)) 
   
    # accuracy
    acc_penalty = 0
    acc_total_cols = len(accuracy_results) if len(accuracy_results) > 0 else 1
    for col, metrics in accuracy_results.items():
        acc_penalty += penalty.get(metrics["status"], 0)
    acc_health = 100 - (acc_penalty / acc_total_cols)

    # consistency
    consist_penalty = 0
    consist_total_rules = len(consistency_results) if len(consistency_results) > 0 else 1
    for issue in consistency_results:
        consist_penalty += penalty.get(issue["status"], 0)
    consist_health = 100 - (consist_penalty / consist_total_rules)

    # uniqueness
    dupe_penalty = penalty.get(duplicate_results["status"], 0)
    dupe_health = 100 - dupe_penalty

    # weighted scoring
    trust_score = (
        (comp_health * weights["comp"]) +
        (valid_health * weights["valid"]) +
        (consist_health * weights["consist"]) +
        (acc_health * weights["acc"]) +
        (dupe_health * weights["dupe"])
    )

    return round(trust_score, 1)

