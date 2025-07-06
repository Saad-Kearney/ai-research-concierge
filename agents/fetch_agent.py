# agents/fetch_agent.py

class FetchAgent:
    def run(self, topic):
        print(f"\n[FetchAgent] Showing curated real links for: '{topic}'")

        # Manually curated real sources (example: topic = EV market India)
        real_links = [
            "https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/ev-market-in-india",
            "https://www.bcg.com/publications/2023/the-future-of-electric-vehicles-in-india",
            "https://www2.deloitte.com/in/en/pages/manufacturing/articles/electric-vehicle-market.html",
            "https://www.iea.org/reports/global-ev-outlook-2024",
        ]

        return real_links
