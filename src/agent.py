"""
Abstract LLM interface for knowledge base QA.
Can be plugged with Claude API, Ollama, or other LLM providers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class RetrievedContext:
    title: str
    content: str
    source: Optional[str] = None


@dataclass
class Answer:
    text: str
    sources: List[RetrievedContext]


class LLMInterface(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    def ask(self, question: str, context: List[RetrievedContext]) -> Answer:
        """Ask a question with retrieved context."""
        pass


class ClaudeAdapter(LLMInterface):
    """Adapter for Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def ask(self, question: str, context: List[RetrievedContext]) -> Answer:
        # TODO: Implement Claude API call
        raise NotImplementedError("Claude adapter not yet implemented")


class OllamaAdapter(LLMInterface):
    """Adapter for Ollama local models."""

    def __init__(self, model: str = "llama2"):
        self.model = model

    def ask(self, question: str, context: List[RetrievedContext]) -> Answer:
        # TODO: Implement Ollama API call
        raise NotImplementedError("Ollama adapter not yet implemented")


class KnowledgeBaseAgent:
    """Main agent that combines retrieval and LLM."""

    def __init__(self, retriever, llm: Optional[LLMInterface] = None):
        self.retriever = retriever
        self.llm = llm

    def set_llm(self, llm: LLMInterface):
        self.llm = llm

    def ask(self, question: str, top_k: int = 3) -> Answer:
        """
        Ask a question about the knowledge base.
        1. Retrieve relevant articles
        2. Build context
        3. Ask LLM (or return raw context if no LLM configured)
        """
        articles = self.retriever.search(question, top_k=top_k)

        retrieved_contexts = [
            RetrievedContext(
                title=a.title,
                content=a.content[:1000],  # Limit content length
                source=a.source
            )
            for a in articles
        ]

        if not self.llm:
            # Fallback: return context without LLM summarization
            ctx_text = "\n\n".join([
                f"## {c.title}\n{c.content}" for c in retrieved_contexts
            ])
            return Answer(
                text=f"[No LLM configured. Here are relevant articles:]\n\n{ctx_text}",
                sources=retrieved_contexts
            )

        return self.llm.ask(question, retrieved_contexts)


def build_prompt(question: str, contexts: List[RetrievedContext]) -> str:
    """Build a prompt with retrieved context."""
    context_text = "\n\n".join([
        f"### {c.title}\n{c.content}" for c in contexts
    ])

    return f"""你是一个知识库助手。请根据以下参考资料回答用户的问题。

## 参考资料
{context_text}

## 用户问题
{question}

请基于参考资料给出回答。如果参考资料中没有相关信息，请说明"根据现有资料无法回答这个问题"。
"""
