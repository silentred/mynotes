"""
BM25-based retrieval for knowledge base articles.
"""

import os
import json
import re
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

try:
    import rank_bm25
except ImportError:
    print("Installing rank_bm25...")
    import subprocess
    subprocess.check_call(["pip", "install", "rank-bm25"])
    import rank_bm25


@dataclass
class Article:
    title: str
    path: str
    content: str
    tags: List[str]
    source: Optional[str] = None


class KnowledgeBase:
    def __init__(self, kb_path: str = "kb"):
        self.kb_path = Path(kb_path)
        self.articles: List[Article] = []
        self.corpus: List[str] = []
        self.tokenized_corpus: List[List[str]] = []
        self._load_articles()

    def _load_articles(self):
        """Load all markdown articles from kb/articles/"""
        articles_dir = self.kb_path / "articles"
        if not articles_dir.exists():
            return

        for md_file in articles_dir.rglob("*.md"):
            article = self._parse_article(md_file)
            if article:
                self.articles.append(article)
                self.corpus.append(article.content)
                self.tokenized_corpus.append(self._tokenize(article.content))

        if self.corpus:
            self.bm25 = rank_bm25.BM25Okapi(self.tokenized_corpus)

    def _parse_article(self, path: Path) -> Optional[Article]:
        """Parse a markdown file with optional frontmatter."""
        try:
            content = path.read_text(encoding="utf-8")

            # Extract frontmatter
            frontmatter = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    fm_text = parts[1]
                    content = parts[2].strip()
                    for line in fm_text.strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            frontmatter[key.strip()] = val.strip()

            title = frontmatter.get("title", path.stem)
            tags_str = frontmatter.get("tags", "")
            tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []
            source = frontmatter.get("source")

            return Article(
                title=title,
                path=str(path),
                content=content,
                tags=tags,
                source=source
            )
        except Exception as e:
            print(f"Error parsing {path}: {e}")
            return None

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        text = text.lower()
        words = re.findall(r'\w+', text)
        return words

    def search(self, query: str, top_k: int = 3) -> List[Article]:
        """Search for the top-k most relevant articles."""
        if not self.corpus:
            return []

        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        return [self.articles[i] for i in top_indices if scores[i] > 0]


def main():
    kb = KnowledgeBase()
    print(f"Loaded {len(kb.articles)} articles")

    if kb.articles:
        print("\nAvailable articles:")
        for a in kb.articles:
            print(f"  - {a.title} ({a.path})")


if __name__ == "__main__":
    main()
