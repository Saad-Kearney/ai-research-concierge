# agents/pov_agent.py

class PoVAgent:
    def run(self, topic):
        return (
            f"Suggested PoV structure for '{topic}':\n"
            f"- What is driving change in the {topic.lower()} landscape?\n"
            "- Key opportunities and potential risks\n"
            "- Strategic moves clients can make\n"
            "- Implementation roadmap or pilot ideas\n"
            "- Metrics to track success"
        )
