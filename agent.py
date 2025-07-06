# agents/fetch_agent.py

class FetchAgent:
    def run(self, topic):
        # Simulated results — Replace with real search in Round 2
        print(f"\n[FetchAgent] Simulating web search for: '{topic}'")
        return [
            f"Report: 'Future of {topic}' - BCG",
            f"Blog: 'Top 5 Trends in {topic}' - McKinsey",
            f"News: 'Recent developments in {topic}' - Bloomberg"
        ]
