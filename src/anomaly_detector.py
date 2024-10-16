import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def detect_anomalies(self, features):
        # Reshape features if necessary
        if len(features.shape) > 2:
            features = features.reshape(features.shape[0], -1)

        # Fit and predict
        self.model.fit(features)
        anomaly_scores = self.model.decision_function(features)

        # Normalize scores to 0-100 range
        normalized_scores = (anomaly_scores - np.min(anomaly_scores)) / (np.max(anomaly_scores) - np.min(anomaly_scores))
        quality_score = np.mean(normalized_scores) * 100

        return quality_score
