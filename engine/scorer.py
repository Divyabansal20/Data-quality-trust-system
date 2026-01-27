def calculate_trust_score(completeness_results, duplicate_results, validity_results, accuracy_results, consistency_results):
    """
    Calculates a final Data Trust Score using 
    Weighted Average x Multiplicative Penalty
    """
    
    if not completeness_results:
        return 0.0
    
    #WEIGHTING STRATEGY
    # We assign weights based on 'analytical readiness'. 
    weights = {
        "comp": 0.25, "valid": 0.25, "consist": 0.20, "acc": 0.15, "dupe": 0.15 
    }
    
    # 2. HEALTH CALCULATION (BASELINE)
    # This function measures what percentage of dataset columns are perfectly clean. 
    def get_health(results_dict):
        if not results_dict:
            return 100.0

        items = results_dict.values() if isinstance(results_dict, dict) else results_dict
        excellent_count = sum(1 for item in items if item.get('status') == 'Excellent')
        return (excellent_count / len(items)) * 100

    comp_health = get_health(completeness_results)
    valid_health = get_health(validity_results)
    acc_health = get_health(accuracy_results)
    consist_health = get_health(consistency_results)
    
    dupe_status = duplicate_results.get("status", "Excellent")
    dupe_health = 100 if dupe_status == "Excellent" else (80 if dupe_status == "Warning" else 50)

    # 3. BASE SCORE (WEIGHTED SUM)
    base_score = (
        (comp_health * weights["comp"]) +
        (valid_health * weights["valid"]) +
        (consist_health * weights["consist"]) +
        (acc_health * weights["acc"]) +
        (dupe_health * weights["dupe"])
    )

    # 4. SMART PENALTY LOGIC (THE MULTIPLIER)
    # use a multiplier instead of subtraction?
    # Linear subtraction is too harsh 
    all_statuses = (
        [i.get('status') for i in completeness_results.values()] +
        [i.get('status') for i in validity_results.values()] +
        [i.get('status') for i in accuracy_results.values()] +
        [i.get('status') for i in consistency_results]
    )
    
    critical_count = all_statuses.count('Critical')
    
    # Apply a 15% reduction for every Critical column found
    penalty_multiplier = 0.85 ** critical_count 

    # Final Trust Score calculation
    final_score = base_score * penalty_multiplier

    final_score = max(0, min(100, final_score))

    return round(final_score, 1)