import math
class MemoryDecayModel:
    def __init__(self, default_stability: float = 2.0):
        self.default_stability = default_stability
    def calculate_retention(self, days_passed: float, stability: float) -> float:
        if stability <= 0:
            return 0.0
        return math.exp(-days_passed / stability)
    def calculate_forgetting_risk(self, days_passed: float, stability: float) -> float:
        retention = self.calculate_retention(days_passed, stability)
        return round(1.0 - retention, 4)
    def update_stability(self, current_stability: float, recall_score: float = 1.0) -> float:
        growth_factor = 1.5 + (recall_score * 0.8)
        new_stability = current_stability * growth_factor
        return round(new_stability, 2)
