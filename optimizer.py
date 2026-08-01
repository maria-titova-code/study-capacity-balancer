from typing import List, Dict, Any
from decay_model import MemoryDecayModel

#Класс для предоставления отдельной учебной темы.
class Topic:
    def __init__(self, name: str, days_passed: float, stability: float, cost_minutes: int):
        self.name = name
        self.days_passed = days_passed #Сколько дней прошло с последнего повторения
        self.stability = stability #Прочность памяти (S)
        self.cost_minutes = cost_minutes #Время на повторение (в минутах)
        
class StudyOptimizer:
    #Алгоритм распределения учебной нагрузки (Рюкзак/Knapsack).
    #Отбирает темы с наивысшим приоритетом в рамках дневного лимита времени.
    
    def __init__(self, decay_model: MemoryDecayModel):
        self.decay_model = decay_model
    #Формирует оптимальный план на день
        
    def optimize_daily_schedule(self, topics: List[Topic], max_daily_minutes: int, target_risk_threshold: float = 0.3, mode: str = "standard") -> Dict[str, Any]:
        scored_topics = []
        for topic in topics:
            #1. Считает риск забывания U(t) по модели Эббингауза.
            risk = self.decay_model.calculate_forgetting_risk(topic.days_passed, topic.stability)
            retention = self.decay_model.calculate_retention(topic.days_passed, topic.stability)
            
            #2. Вычисляет приоритет: Priority = Risk / Cost.
            if mode == "cramming":
                priority = risk
            else:
                priority = risk / topic.cost_minutes if topic.cost_minutes > 0 else 0.0
            scored_topics.append({
                'topic': topic,
                'risk': risk,
                'retention': retention,
                'priority': priority
            })
        #3. Заполняет доступное время наиболее критичными темами.
        scored_topics.sort(key=lambda x: x['priority'], reverse=True)
        scheduled_today = []
        deferred_topics = []
        total_time_used = 0
        
        # 4. Упаковка тем в дневной лимит времени
        for item in scored_topics:
            t = item['topic']
            risk = item['risk']
            if total_time_used + t.cost_minutes <= max_daily_minutes:
                scheduled_today.append({
                    "name": t.name,
                    "cost_minutes": t.cost_minutes,
                    "forgetting_risk": f"{risk * 100:.1f}%",
                    "retention": f"{item['retention'] * 100:.1f}%",
                    "raw_risk": risk,
                    "stability": t.stability,
                    "days_passed": t.days_passed
                })
                total_time_used += t.cost_minutes
            else:
                deferred_topics.append({
                    "name": t.name,
                    "cost_minutes": t.cost_minutes,
                    "forgetting_risk": f"{risk * 100:.1f}%",
                    "retention": f"{item['retention'] * 100:.1f}%",
                    "raw_risk": risk,
                    "stability": t.stability,
                    "days_passed": t.days_passed
                })
        return {
            'scheduled_today': scheduled_today,
            'total_time_used': total_time_used,
            'max_capacity': max_daily_minutes,
            'deferred_topics': deferred_topics
        }
