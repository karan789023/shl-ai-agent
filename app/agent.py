from services.retriever import Retriever
from services.llm import GeminiLLM
import json

class AIAgent:
    def __init__(self, catalog, api_key):
        self.retriever = Retriever(catalog, use_saved=False)
        self.llm = GeminiLLM(api_key)

    def parse_requirements(self, query):
        return {
            "skill": query,
            "level": "unknown",
            "intent": "search"
        }

    def run(self, query):

        results = self.retriever.search(query)

        final_response = self.llm.generate_response(query, results)

        return {
            "query": query,
            "results": results,
            "response": final_response
        }