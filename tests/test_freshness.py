import numpy as np
from freshness import FreshnessDetector

def test_assess_freshness():
    detector = FreshnessDetector()
    features = np.array([0.5, 0.7, 0.3])
    score = detector.assess_freshness(features)
    assert 0 <= score <= 100

    # Test edge cases
    assert detector.assess_freshness(np.array([0, 0, 0])) == 0
    assert detector.assess_freshness(np.array([1, 1, 1])) == 100
    assert detector.assess_freshness(np.array([-1, 0.5, 2])) == 50
