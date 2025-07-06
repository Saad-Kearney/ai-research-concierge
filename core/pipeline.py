# core/pipeline.py

from agents.fetch_agent import FetchAgent
from agents.summary_agent import SummaryAgent
from agents.pov_agent import PoVAgent

def run_pipeline():
    topic = input("🔎 Enter your research topic: ")

    fetch_agent = FetchAgent()
    summary_agent = SummaryAgent()
    pov_agent = PoVAgent()

    sources = fetch_agent.run(topic)
    print("\n📚 Sources:")
    for s in sources:
        print(" -", s)

    summary = summary_agent.run(sources)
    print("\n📝 Summary:")
    print(summary)

    pov = pov_agent.run(topic)
    print("\n📊 Point-of-View Structure:")
    print(pov)
