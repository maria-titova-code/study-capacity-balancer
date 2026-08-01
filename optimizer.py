from typing import List, Dict, Any
from decay_model import MemoryDecayModel

class Topic:
    def __init__(self, name: str, days_since_review: float, stability: float, cost_minutes: int):
        self.name = name
        self.days_since_review = days_since_review
        self.stability = stability
        self.cost_minutes = cost_minutes
class StudyOptimizer:
    def __init__(self, decay_model: MemoryDecayModel):
        self.decay_model = decay_model
    def optimize_daily_schedule(self, topics: List[Topic], max_daily_minutes: int) -> Dict[str, Any]:
        scored_topics = []
        for topic in topics:
            risk = self.decay_model.calculate_forgetting_risk(
                topic.days_since_review,
                topic.stability
            )
            priority = risk / topic.cost_ minutes
            if topic.cost_minutes > 0
            else 0
            scored_topics.append({
                'topic': topic,
                'risk': risk,
                'priority': priority
            })
        scored_ topics.sort(key=lambda x: x['priority'], reverse=True)
        selected_topics = []
        deferred_topics = []
        total_time = 0

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
