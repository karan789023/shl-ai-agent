from app.agent import AIAgent
from services.retriever import load_catalog
import json


catalog = load_catalog()
agent = AIAgent(catalog, api_key="AIzaSyAaGg5QFMNRNQlIWJBKPdKB1b-GPUaxSD8")


with open("tests/test_queries.json", "r") as f:
    test_queries = json.load(f)


for q in test_queries:
    print("\n" + "="*60)
    print("QUERY:", q)

    result = agent.run(q)

    print("\nRESPONSE:\n")
    print(result["response"])