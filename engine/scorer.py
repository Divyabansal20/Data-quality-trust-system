
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
    
    completeness_penalty=0
    for cols, metric in completeness_results.items():
        completeness_penalty+=penalty.get(metric['status'],0)
    comp_health= 100- (completeness_penalty / len(completeness_results))

    valid_penalty=0
    for col, metrics in validity_results.items():
        valid_penalty += penalty.get(metrics["status"], 0)
    valid_health = 100 - (valid_penalty / len(validity_results)) 

    acc_penalty = 0
    acc_total_cols = len(accuracy_results) if len(accuracy_results) > 0 else 1
    for col, metrics in accuracy_results.items():
        acc_penalty += penalty.get(metrics["status"], 0)
    acc_health = 100 - (acc_penalty / acc_total_cols)

    consist_penalty = 0
    consist_total_rules = len(consistency_results) if len(consistency_results) > 0 else 1
    for issue in consistency_results:
        consist_penalty += penalty.get(issue["status"], 0)
    consist_health = 100 - (consist_penalty / consist_total_rules)

    dupe_penalty = penalty.get(duplicate_results["status"], 0)
    dupe_health = 100 - dupe_penalty


    trust_score = (
        (comp_health * weights["comp"]) +
        (valid_health * weights["valid"]) +
        (consist_health * weights["consist"]) +
        (acc_health * weights["acc"]) +
        (dupe_health * weights["dupe"])
    )

    return round(trust_score, 1)



    # for cols, metrics in completeness_results.items():
    #     if metrics["status"]=="Critical":
    #         total_penalty+=30
    #     elif metrics["status"]=="Warning":
    #         total_penalty+=10
    # average_penalty= total_penalty/total_cols

    # # file penalties on duplicates
    # file_penalty=0
    # if duplicate_results["status"]=="Warning":
    #     file_penalty = 10
    # elif duplicate_results["status"] == "Critical":
    #     file_penalty = 25

    # # validity penalty 
    # validity_penalty = 0
    # for col, metrics in validity_results.items(): 
    #     if metrics["status"] == "Critical":
    #         validity_penalty += 20  
    #     elif metrics["status"] == "Warning":
    #         validity_penalty += 5

    # avg_validity_penalty = validity_penalty / total_cols


    # # accuracy_results 
    # accuracy_penalty=0
    # for col, metrics in accuracy_results.items(): 
    #     if metrics["status"] == "Critical":
    #         accuracy_penalty += 20  
    #     elif metrics["status"] == "Warning":
    #         accuracy_penalty += 5
    # if len(accuracy_results)>0:
    #     average_accuracy_penalty= accuracy_penalty/len(accuracy_results)
    # else:
    #     average_accuracy_penalty=0

    # # Consistency 
    # consist_penalty = 0
    # for issue in consistency_results:
    #     if issue["status"] == "Warning":
    #         consist_penalty += 10  
    #     elif issue["status"] == "Critical":
    #         consist_penalty += 20
    # consist_penalty = min(consist_penalty, 30)

    # total_damage = average_penalty + file_penalty + avg_validity_penalty + average_accuracy_penalty+ consist_penalty

    # # final score
    # final_score = max(0, 100 - total_damage)
    
    # return round(final_score, 1)
