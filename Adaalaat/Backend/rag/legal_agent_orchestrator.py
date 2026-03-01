"""
Legal Agent Orchestrator

Implements an Agentic RAG pipeline for legal advisory.

Architecture:
    ┌─────────────┐       ┌───────────────┐
    │   Decider    │──────▶│  RAG Search   │──▶ Local PDF (in-memory)
    │   (Router)   │       └───────────────┘
    │              │       ┌───────────────┐
    │              │──────▶│  Web Search   │──▶ Serper API
    └──────┬───────┘       └───────────────┘
           │
    ┌──────▼───────┐
    │  Synthesizer │──▶ Final Legal Advisory (Llama-3.1-8B)
    └──────────────┘

Pipeline:
    1. Decider classifies the query → LEGAL_RAG / WEB_SEARCH / BOTH / GENERAL
    2. RAG search retrieves from the local PDF embeddings
    3. Web search queries the web
    4. Synthesizer (Llama-3.1-8B) merges context into a legal advisory
"""

import os
import json
import logging
from typing import List, Optional

from llama_index.core.llms import ChatMessage

from rag.local_pdf_retriever import search as pdf_search
from rag.web_search_service import WebSearchService

logger = logging.getLogger(__name__)


class LegalAgentOrchestrator:
    """
    Legal advisory pipeline using Llama-3.1-8B via HuggingFace Inference API.

    Uses direct tool calls (no FunctionAgent) for maximum compatibility.
    """

    def __init__(self, config_path: str, llm):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.web_search_service = WebSearchService(config_path=config_path)
        self.llm = llm

        # Pre-load the PDF embeddings on init
        logger.info("Pre-loading legal document embeddings...")
        try:
            from rag.local_pdf_retriever import _ensure_loaded
            _ensure_loaded()
            logger.info("Legal document embeddings ready ✓")
        except Exception as e:
            logger.warning(f"Could not pre-load PDF (will retry on first query): {e}")

        # ── System Prompts ──────────────────────────────────────
        self.decider_prompt = """You are the routing agent for a Legal Advisory Chatbot. Analyze the user's query and chat history to decide the best action.

Respond ONLY with a single, valid JSON object (no markdown, no explanation):
{"decision": "LEGAL_RAG", "search_query": "the rewritten search query"}

Rules for the "decision" field:
- LEGAL_RAG: For questions about laws, tenant rights, property disputes, divorce, consumer rights, etc.
- WEB_SEARCH: For highly recent events or verifying if a specific new bill has passed recently.
- BOTH: If comparing established law with recent news.
- GENERAL: For greetings or meta-questions.

Rules for "search_query": rewrite the user's query into a clear, standalone legal search query. If GENERAL, set to null."""

        self.synthesizer_prompt = """You are an AI Legal Assistant for the Adaalat legal advisory platform. Your job is to synthesize the provided legal context into a helpful advisory response.

CRITICAL RULES:
1. You are an AI, not a licensed attorney. Include a brief disclaimer.
2. Synthesize the provided legal statutes and context clearly.
3. If the context does not contain the answer, state that explicitly. Do NOT hallucinate laws.
4. Structure your response clearly with:
   - The relevant legal area
   - A clear analysis of the situation
   - Concrete recommended next steps
   - Relevant statutes or laws cited (if found in context)
5. Be empathetic but factual."""

        self.last_search_sources = []

    # ── Direct Tool Calls ───────────────────────────────────────

    def _search_legal_database(self, query: str) -> str:
        """Search the local PDF using in-memory cosine similarity."""
        logger.info(f"[RAG] Searching local PDF for: '{query}'")
        self.last_search_sources = []

        try:
            chunk_top_k = self.config.get("rag_agent", {}).get("chunk_top_k", 8)
            results = pdf_search(query, top_k=chunk_top_k)

            if not results:
                return "No relevant statutes or precedents found in the legal document."

            formatted_chunks = []
            for r in results:
                formatted_chunks.append(f"[Source: {r['source']}]\n{r['text']}")
                self.last_search_sources.append({
                    "source": r["source"],
                    "relevance_score": r["score"],
                })

            logger.info(f"[RAG] Found {len(results)} relevant chunks")
            return "\n\n---\n\n".join(formatted_chunks)

        except Exception as e:
            logger.error(f"[RAG] Local PDF search failed: {e}")
            return f"Search failed: {str(e)}"

    def _perform_web_search(self, query: str) -> str:
        """Perform a web search for recent legal information."""
        logger.info(f"[WEB] Searching web for: '{query}'")

        try:
            results = self.web_search_service.search(query)
            logger.info("[WEB] Web search completed")
            return results
        except Exception as e:
            logger.error(f"[WEB] Web search failed: {e}")
            return f"Web search failed: {str(e)}"

    def _normalize_chat_history(self, history: list) -> List[ChatMessage]:
        """Normalize chat history into LlamaIndex ChatMessage format."""
        messages = []
        for msg in history:
            if isinstance(msg, ChatMessage):
                messages.append(msg)
            elif isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                messages.append(ChatMessage(role=role, content=content))
        return messages

    # ── Main Pipeline ───────────────────────────────────────────

    async def run_async(
        self,
        query: str,
        allow_web: bool = True,
        history: Optional[list] = None,
    ):
        """
        Execute the legal reasoning pipeline.

        Steps:
            1. Decider classifies the query (LLM call)
            2. Direct tool calls to retrieve context
            3. Synthesizer generates the final advisory (LLM call)
        """
        logger.info(f"\n--- New Legal Query: '{query}' ---")
        history = history or []
        normalized_history = self._normalize_chat_history(history)

        # ── 1. Decider Phase ────────────────────────────────────
        decider_messages = [
            ChatMessage(role="system", content=self.decider_prompt),
            *normalized_history,
            ChatMessage(role="user", content=query),
        ]

        try:
            decision_response = await self.llm.achat(messages=decider_messages)
            raw_content = decision_response.message.content.strip()
            logger.info(f"[DECIDER] Raw response: {raw_content[:200]}")

            # Extract JSON from the response (handle markdown code blocks)
            if "```" in raw_content:
                raw_content = raw_content.split("```")[1]
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:]
                raw_content = raw_content.strip()

            decision_json = json.loads(raw_content)
            decision = decision_json.get("decision", "GENERAL").upper()
            search_query = decision_json.get("search_query", query)
            logger.info(f"[DECIDER] Decision: {decision}, Search: {search_query}")
        except Exception as e:
            logger.warning(f"[DECIDER] Failed to parse, defaulting to LEGAL_RAG: {e}")
            decision, search_query = "LEGAL_RAG", query

        context = ""
        self.last_search_sources = []

        # ── 2. Direct Tool Calls ────────────────────────────────
        if decision in ["LEGAL_RAG", "BOTH"]:
            rag_result = self._search_legal_database(search_query)
            context += f"Legal Database Context:\n{rag_result}\n\n"

        if decision in ["WEB_SEARCH", "BOTH"] and allow_web:
            web_result = self._perform_web_search(search_query)
            context += f"Web Search Results:\n{web_result}\n\n"

        # ── 3. Synthesis Phase ──────────────────────────────────
        if decision == "GENERAL":
            messages = [
                ChatMessage(role="system", content=self.synthesizer_prompt),
                *normalized_history,
                ChatMessage(role="user", content=query),
            ]
            final_response = await self.llm.achat(messages=messages)
            return {"answer": final_response.message.content, "sources": []}

        synthesis_messages = [
            ChatMessage(
                role="system",
                content=f"{self.synthesizer_prompt}\n\nRelevant Legal Context:\n{context}",
            ),
            *normalized_history,
            ChatMessage(role="user", content=query),
        ]

        logger.info("[SYNTH] Generating final advisory...")
        final_response = await self.llm.achat(messages=synthesis_messages)
        logger.info("[SYNTH] Advisory generated ✓")

        return {
            "answer": final_response.message.content,
            "sources": self.last_search_sources,
        }
