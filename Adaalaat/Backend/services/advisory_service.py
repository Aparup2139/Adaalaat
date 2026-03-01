"""
Advisory Service
Orchestrates the Agentic RAG pipeline via LegalAgentOrchestrator.

Uses HuggingFace Inference API for both LLM (Llama-3.1-8B) and
embeddings (BAAI/bge-small-en-v1.5) — no local models needed.
"""

import os
import asyncio
import logging
from rag.legal_agent_orchestrator import LegalAgentOrchestrator
from utils.helpers import classify_legal_domain

logger = logging.getLogger(__name__)

# ── Singleton orchestrator instance ─────────────────────────────
_orchestrator = None


def _get_orchestrator():
    """Lazy-initialize the LegalAgentOrchestrator with HF Inference LLM."""
    global _orchestrator

    if _orchestrator is None:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

        # Initialize HF Inference LLM (remote API — no local download)
        try:
            import json
            from rag.hf_inference_llm import HFInferenceLLM

            with open(config_path, "r") as f:
                config = json.load(f)

            llm_config = config.get("llm", {})
            llm = HFInferenceLLM(
                model_name=llm_config.get("model_name", "meta-llama/Llama-3.1-8B-Instruct:novita"),
                hf_token=os.environ.get("HUGGINGFACE_TOKEN", "") or os.environ.get("HF_TOKEN", ""),
                max_tokens=llm_config.get("max_new_tokens", 1024),
                temperature=llm_config.get("temperature", 0.3),
            )
            logger.info(f"LLM initialized: {llm.model_name}")

        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

        _orchestrator = LegalAgentOrchestrator(
            config_path=config_path,
            llm=llm,
        )
        logger.info("LegalAgentOrchestrator initialized")

    return _orchestrator


class AdvisoryService:

    @staticmethod
    def process_query(query_text, user_id=None, history=None):
        """
        Process a client's legal query through the Agentic RAG pipeline.

        Uses the LegalAgentOrchestrator which runs:
            1. Decider → classifies query type (via Llama-3.1-8B)
            2. RAG Worker → retrieves from local PDF (via BGE embeddings)
            3. Web Worker → searches web (if needed)
            4. Synthesizer → generates final advisory (via Llama-3.1-8B)

        Args:
            query_text: The client's description of their legal situation
            user_id: Optional user ID for session tracking
            history: Optional list of previous chat messages

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            orchestrator = _get_orchestrator()

            # Run the async orchestrator in a sync context
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()

            result = asyncio.run(
                orchestrator.run_async(
                    query=query_text,
                    allow_web=True,
                    history=history or [],
                )
            )

            # Parse the orchestrator response
            answer = result.get("answer", "")
            sources = result.get("sources", [])

            # Classify the legal domain
            area = classify_legal_domain(query_text)

            # Extract steps from the answer
            steps = _extract_steps(answer)

            # Extract statutes from sources
            relevant_statutes = [
                s["source"] for s in sources if s.get("source")
            ]

            return {
                "area": area,
                "analysis": answer,
                "steps": steps,
                "relevantStatutes": relevant_statutes,
                "sources": sources,
                "disclaimer": (
                    "This is an AI-generated preliminary advisory and does not "
                    "constitute legal advice. Please consult a qualified lawyer "
                    "for professional guidance."
                ),
            }, None

        except Exception as e:
            logger.error(f"Advisory generation failed: {e}")
            return None, f"Advisory generation failed: {str(e)}"


def _extract_steps(answer: str) -> list:
    """Extract recommended steps from the LLM answer."""
    import re

    numbered = re.findall(r"\d+\.\s+(.+?)(?=\n\d+\.|\n\n|$)", answer, re.DOTALL)
    if numbered and len(numbered) >= 2:
        return [step.strip() for step in numbered[:6]]

    bullets = re.findall(r"[-•]\s+(.+?)(?=\n[-•]|\n\n|$)", answer, re.DOTALL)
    if bullets and len(bullets) >= 2:
        return [step.strip() for step in bullets[:6]]

    return [
        "Document all relevant facts and timeline of events",
        "Collect supporting evidence and correspondence",
        "Consult with a qualified lawyer specialized in this area",
        "Explore alternative dispute resolution before litigation",
    ]
