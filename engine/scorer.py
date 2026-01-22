
def calculate_trust_score(completeness_results, duplicate_results, validity_results, accuracy_results, consistency_results):
    if not completeness_results:
        return 0.0
    
    penalty_map = {
        'Excellent': 0,
        'Warning': 5,
        'Critical': 15 
    }
    
    weights = {
        "comp": 0.25,  "valid": 0.25, "consist": 0.20, "acc": 0.15, "dupe": 0.15 
    }
    
    def get_health(results_dict):
        if not results_dict:
            return 100.0
        # Handle both lists (consistency) and dicts (others)
        items = results_dict.values() if isinstance(results_dict, dict) else results_dict
        total_penalty = sum(penalty_map.get(item['status'], 0) for item in items)
        return max(0, 100 - (total_penalty / len(items)))

    comp_health = get_health(completeness_results)
    valid_health = get_health(validity_results)
    acc_health = get_health(accuracy_results)
    consist_health = get_health(consistency_results)
    
    dupe_penalty = penalty_map.get(duplicate_results.get("status"), 0)
    dupe_health = 100 - dupe_penalty

    trust_score = (
        (comp_health * weights["comp"]) +
        (valid_health * weights["valid"]) +
        (consist_health * weights["consist"]) +
        (acc_health * weights["acc"]) +
        (dupe_health * weights["dupe"])
    )

    return round(trust_score, 1)