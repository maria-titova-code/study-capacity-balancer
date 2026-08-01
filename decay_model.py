import math
#Математическая модель спада Эббингауза.
class MemoryDecayModel:
    #Позволяет расчитать вероятность сохранения информации в памяти и риск её забывания со временем.

    def __init__(self, default_stability: float = 2.0):
        #default_stability(S) - начальная прочность памяти (в днях)
        self.default_stability = default_stability

    def calculate_retention(self, days_passed: float, stability: float) -> float:
        #Расчёт вероятности воспоминания R(t) через t дней. Формула: R(t) = exp(-t/S)
        if stability <= 0:
            return 0.0
        return math.exp(-days_passed / stability)

    def calculate_forgetting_risk(self, days_passed: float, stability: float) -> float:
        #Расчёт коэффициента риска забывания: U(t) = 1-R(t). Возвращает значение от 0.0 (свежая память) до 1.0 (забыто полностью)
        retention = self.calculate_retention(days_passed, stability)
        return round(1.0 - retention, 4)

    def update_stability(self, current_stability: float, recall_score: float = 1.0) -> float:
        #Перерасчет прочности памяти (S) после успешного повторения.
        #recall_score: оценка качества ответа (от 0.0 до 1.0)
        growth_factor = 1.5 + (recall_score * 0.8)
        #С каждым повторением прочность памяти увеличивается
        new_stability = current_stability * growth_factor
        return round(new_stability, 2)

    def update_stability_after_review(self, current_stability: float, multiplier: float = 1.5) -> float:
        #Увеличивает прочность памяти (S) после успешного повторения.
        return round(current_stability * multiplier, 2)
