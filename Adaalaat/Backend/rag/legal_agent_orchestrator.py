"""
Legal Agent Orchestrator

Implements an Agentic RAG pipeline for legal advisory.

Architecture:
    ┌─────────────┐       ┌───────────────┐
    │   Decider    │──────▶│  RAG Search   │──▶ Local PDF (in-memory)
    │   (Router)   │       └───────────────┘
    └──────┬───────┘
           │
    ┌──────▼───────┐
    │  Synthesizer │──▶ Final Legal Advisory (Llama-3.1-8B)
    └──────────────┘

Pipeline:
    1. Decider classifies the query → LEGAL_RAG / GENERAL
    2. RAG search retrieves from the local PDF embeddings
    3. If RAG yields no results, the LLM responds from its own knowledge
       with a disclaimer (LLM fallback)
    4. Synthesizer (Llama-3.1-8B) merges context into a legal advisory
"""

import os
import json
import logging
from typing import List, Optional

from llama_index.core.llms import ChatMessage

from rag.local_pdf_retriever import search as pdf_search

logger = logging.getLogger(__name__)


class LegalAgentOrchestrator:
    """
    Legal advisory pipeline using Llama-3.1-8B via HuggingFace Inference API.

    Uses direct tool calls (no FunctionAgent) for maximum compatibility.
    """

    def __init__(self, config_path: str, llm):
        with open(config_path, "r") as f:
            self.config = json.load(f)

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
- LEGAL_RAG: For questions about laws, tenant rights, property disputes, divorce, consumer rights, legal procedures, statutes, or any legal topic.
- GENERAL: For greetings, meta-questions, or non-legal queries.

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

        self.llm_fallback_prompt = """You are an AI Legal Assistant for the Adaalat legal advisory platform. The user asked a legal question, but no relevant documents were found in our local legal database.

CRITICAL RULES:
1. You are an AI, not a licensed attorney. Include a brief disclaimer.
2. Answer using your general legal knowledge to the best of your ability.
3. CLEARLY STATE at the beginning of your response that this answer is based on general AI knowledge and NOT from verified legal documents in our database.
4. Structure your response clearly with:
   - The relevant legal area
   - A clear analysis of the situation
   - Concrete recommended next steps
   - Any relevant statutes or laws you are aware of (cite them carefully)
5. Strongly recommend consulting a qualified lawyer for verified legal advice.
6. Be empathetic but factual."""

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
                return ""

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
            return ""

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
        history: Optional[list] = None,
    ):
        """
        Execute the legal reasoning pipeline.

        Steps:
            1. Decider classifies the query (LLM call)
            2. Direct tool calls to retrieve context
            3. If RAG returns results → Synthesizer merges them into advisory
            4. If RAG returns nothing → LLM fallback from general knowledge
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

        self.last_search_sources = []

        # ── 2. Direct Tool Calls ────────────────────────────────
        if decision == "GENERAL":
            messages = [
                ChatMessage(role="system", content=self.synthesizer_prompt),
                *normalized_history,
                ChatMessage(role="user", content=query),
            ]
            final_response = await self.llm.achat(messages=messages)
            return {"answer": final_response.message.content, "sources": []}

        # ── 3. RAG Search ───────────────────────────────────────
        rag_result = self._search_legal_database(search_query)

        # ── 4. Synthesis / LLM Fallback ─────────────────────────
        if rag_result:
            # RAG returned context → synthesize with it
            synthesis_messages = [
                ChatMessage(
                    role="system",
                    content=f"{self.synthesizer_prompt}\n\nRelevant Legal Context:\n{rag_result}",
                ),
                *normalized_history,
                ChatMessage(role="user", content=query),
            ]
            logger.info("[SYNTH] Generating final advisory with RAG context...")
        else:
            # No RAG results → fall back to LLM general knowledge
            synthesis_messages = [
                ChatMessage(role="system", content=self.llm_fallback_prompt),
                *normalized_history,
                ChatMessage(role="user", content=query),
            ]
            logger.info("[FALLBACK] No RAG results — using LLM general knowledge...")

        final_response = await self.llm.achat(messages=synthesis_messages)
        logger.info("[SYNTH] Advisory generated ✓")

        return {
            "answer": final_response.message.content,
            "sources": self.last_search_sources,
        }
