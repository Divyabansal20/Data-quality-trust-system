def calculate_trust_score(audit_result):
    if not audit_result:
        return 0
    total_cols= len(audit_result)
    total_penalty=0
    for cols, metrics in audit_result.items():
        if metrics["status"]=="Critical":
            total_penalty+=10
        elif metrics["status"]=="Warning":
            total_penalty+=30
    average_penalty= total_penalty/total_cols
    final_score = max(0, 100 - average_penalty)
    
    return round(final_score, 1)
