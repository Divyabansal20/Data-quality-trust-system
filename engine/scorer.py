
def calculate_trust_score(completeness_results,duplicate_results,validity_results, accuracy_results):

    if not completeness_results:
        return 0
    
    # column penalities on completeness
    total_cols= len(completeness_results)
    total_penalty=0

    for cols, metrics in completeness_results.items():
        if metrics["status"]=="Critical":
            total_penalty+=30
        elif metrics["status"]=="Warning":
            total_penalty+=10
    average_penalty= total_penalty/total_cols

    # file penalties on duplicates
    if duplicate_results["status"]=="Warning":
        file_penalty = 10
    elif duplicate_results["status"] == "Critical":
        file_penalty = 25

    # validity penalty 
    validity_penalty = 0
    for col, metrics in validity_results.items(): 
        if metrics["status"] == "Critical":
            validity_penalty += 20  
        elif metrics["status"] == "Warning":
            validity_penalty += 5

    avg_validity_penalty = validity_penalty / total_cols


    # accuracy_results 
    accuracy_penalty=0
    for col, metrics in accuracy_results.items(): 
        if metrics["status"] == "Critical":
            accuracy_penalty += 20  
        elif metrics["status"] == "Warning":
            accuracy_penalty += 5


    total_damage = average_penalty + file_penalty + avg_validity_penalty + accuracy_penalty

    # final score
    final_score = max(0, 100 - total_damage)
    
    return round(final_score, 1)
