from typing import List, Dict, Any
from decay_model import MemoryDecayModel

#Класс для предоставления отдельной учебной темы.
class Topic:
    def __init__(self, name: str, days_since_review: float, stability: float, cost_minutes: int):
        self.name = name
        self.days_since_review = days_since_review #Сколько дней прошло с последнего повторения
        self.stability = stability #Прочность памяти (S)
        self.cost_minutes = cost_minutes #Время на повторение (в минутах)
class StudyOptimizer:
    #Алгоритм распределения учебной нагрузки (Рюкзак/Knapsack).
    #Отбирает темы с наивысшим приоритетом в рамках дневного лимита времени.
    def __init__(self, decay_model: MemoryDecayModel):
        self.decay_model = decay_model
    #Формирует оптимальный план на день    
    def optimize_daily_schedule(self, topics: List[Topic], max_daily_minutes: int) -> Dict[str, Any]:
        scored_topics = []
        for topic in topics:
            #1. Считает риск забывания U(t) по модели Эббингауза.
            risk = self.decay_model.calculate_forgetting_risk(
                topic.days_since_review,
                topic.stability
            )
            #2. Вычисляет приоритет: Priority = Risk / Cost.
            if topic.cost_minutes > 0:
                priority = risk / topic.cost_minutes
            else:
                priority = 0.0
            scored_topics.append({
                'topic': topic,
                'risk': risk,
                'priority': priority
            })
        #3. Заполняет доступное время наиболее критичными темами.
        scored_topics.sort(key=lambda x: x['priority'], reverse=True)
        selected_topics = []
        deferred_topics = []
        total_time = 0

        # 4. Упаковка тем в дневной лимит времени
        for item in scored_topics:
            topic = item['topic']
            if total_time + topic.cost_minutes <= max_daily_minutes:
                selected_topics.append({
                    'name': topic.name,
                    'cost_minutes': topic.cost_minutes,
                    'forgetting_risk': f"{round(item['risk']*100, 1)}%"
                })
                total_time += topic.cost_minutes
            else:
                deferred_topics.append({
                    'name': topic.name,
                    'forgetting_risk': f"{round(item['risk']*100, 1)}%"
                })
        return {
            'scheduled_today': selected_topics,
            'total_time_used': total_time,
            'max_capacity': max_daily_minutes,
            'deferred_topics': deferred_topics
        }
