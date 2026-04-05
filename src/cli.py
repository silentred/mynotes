#!/usr/bin/env python3
"""
Simple CLI for querying the knowledge base.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.retriever import KnowledgeBase
from src.agent import KnowledgeBaseAgent, ClaudeAdapter, OllamaAdapter


def main():
    kb = KnowledgeBase()
    agent = KnowledgeBaseAgent(kb)

    # Check if LLM is configured
    llm_type = os.environ.get("KB_LLM", "none")
    if llm_type == "claude":
        agent.set_llm(ClaudeAdapter())
        print("Using Claude API for answers")
    elif llm_type == "ollama":
        agent.set_llm(OllamaAdapter())
        print("Using Ollama for answers")
    else:
        print("No LLM configured (set KB_LLM=claude or KB_LLM=ollama)")
        print()

    print(f"Knowledge base loaded: {len(kb.articles)} articles")
    print()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"Q: {question}")
        print()
        answer = agent.ask(question)
        print(f"A: {answer.text}")
    else:
        print("Usage: python -m src.cli \"your question\"")
        print()
        print("Available articles:")
        for a in kb.articles:
            print(f"  - {a.title}")


if __name__ == "__main__":
    main()
