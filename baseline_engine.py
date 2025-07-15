from features_config import features

# These categorical features are always critical
strict_features = ["ip_country"]

# Optional weights (can be tuned per feature)
feature_weights = {
    "typing_speed": 2.0,
    "click_rate": 1.0,
    "mouse_speed": 1.0,
    "scroll_ratio": 1.0,
}

def detect_anomaly(user_id, current_session, baselines, threshold=0.35, critical_deviation_threshold=0.35):
    """
    Compare current session with baseline and return anomaly status and score.

    Args:
        user_id (str): User identifier.
        current_session (dict): Current session's feature values.
        baselines (dict): Stored baseline data for all users.
        threshold (float): Threshold to flag anomaly.
        critical_deviation_threshold (float): If any feature deviates beyond this, trigger instantly.

    Returns:
        (str, float): ("Normal" or "Anomaly", score between 0-1)
    """
    baseline = baselines.get(user_id)
    if not baseline:
        return "No baseline", 0.0

    score = 0.0
    total_weight = 0.0

    for feat in features:
        base = baseline.get(feat)
        curr = current_session.get(feat)

        if base is None or curr is None:
            continue

        weight = feature_weights.get(feat, 1.0)

        # STRICT: categorical mismatch (like ip_country) triggers instantly
        if feat in strict_features:
            if base != curr:
                print(f"[STRICT] {feat} mismatch: {base} → {curr}")
                return "Anomaly", 1.0

        # NUMERIC FEATURE: scaled deviation
        if isinstance(base, (int, float)) and isinstance(curr, (int, float)):
            deviation = abs(curr - base) / (abs(base) + 1e-6)
            print(f"{feat} deviation: {deviation:.3f}")

            # If too extreme, trigger immediately
            if deviation > critical_deviation_threshold:
                print(f"[CRITICAL] {feat} deviation {deviation:.3f} exceeds {critical_deviation_threshold}")
                return "Anomaly", 1.0

            # Scaled scoring (only if deviation > 0.2)
            if deviation > 0.2:
                scaled = min(deviation, 1.0)
                score += weight * scaled
                total_weight += weight  # Only include if deviation significant

        # CATEGORICAL FEATURE (non-strict ones)
        elif base != curr:
            score += weight
            total_weight += weight

    final_score = score / total_weight if total_weight > 0 else 0.0
    status = "Anomaly" if final_score > threshold else "Normal"
    print(f"→ Final Score: {final_score:.3f}")
    return status, final_score
