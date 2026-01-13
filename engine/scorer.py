
def calculate_trust_score(completeness_results,duplicate_results):

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
        file_penalty = 25
    elif duplicate_results["status"] == "Critical":
        file_penalty = 10


    total_damage= average_penalty+ file_penalty
    # final score
    final_score = max(0, 100 - total_damage)
    return round(final_score, 1)
