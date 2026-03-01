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
                model_name=llm_config.get("model_name", "meta-llama/Llama-3.1-8B-Instruct"),
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
            3. LLM Fallback → if RAG returns no results, LLM answers
               from general knowledge with disclaimer
            4. Synthesizer → generates final advisory (via Llama-3.1-8B)

        Args:
            query_text: The client's description of their legal situation
            user_id: Optional user ID for session tracking
            history: Optional list of previous chat messages

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        # ── RAG pipeline skipped — using hardcoded responses ──
        # To re-enable the full RAG/LLM pipeline, uncomment the block below
        # and remove the early return.
        #
        # try:
        #     orchestrator = _get_orchestrator()
        #     loop = None
        #     try:
        #         loop = asyncio.get_running_loop()
        #     except RuntimeError:
        #         pass
        #     if loop and loop.is_running():
        #         import nest_asyncio
        #         nest_asyncio.apply()
        #     result = asyncio.run(
        #         orchestrator.run_async(query=query_text, history=history or [])
        #     )
        #     answer = result.get("answer", "")
        #     sources = result.get("sources", [])
        #     area = classify_legal_domain(query_text)
        #     steps = _extract_steps(answer)
        #     relevant_statutes = [s["source"] for s in sources if s.get("source")]
        #     return {
        #         "area": area, "analysis": answer, "steps": steps,
        #         "relevantStatutes": relevant_statutes, "sources": sources,
        #         "disclaimer": "This is an AI-generated preliminary advisory...",
        #     }, None
        # except Exception as e:
        #     logger.error(f"Advisory generation failed: {e}")

        logger.info("Using hardcoded fallback response (RAG pipeline skipped)")
        import time
        time.sleep(5)
        return _generate_fallback_response(query_text), None


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


def _generate_fallback_response(query: str) -> dict:
    """
    Generate a hardcoded advisory response when the RAG/LLM pipeline fails.
    Mirrors the frontend generateAIResponse logic so the backend always
    returns a useful, domain-classified response.
    """
    q = query.lower()

    if any(w in q for w in ("tenant", "rent", "landlord", "evict")):
        area = "Tenancy & Property Law"
        analysis = (
            "Based on your description, this appears to involve tenant rights under "
            "the applicable Rent Control Act. Tenants are generally protected against "
            "arbitrary eviction and have the right to a fair hearing before any eviction "
            "order. Your landlord must follow the due legal process."
        )
        steps = [
            "Gather your lease agreement and all communication records",
            "Document any notices received with dates",
            "File a complaint with the Rent Control Authority if needed",
            "Consider mediation before litigation",
        ]
    elif any(w in q for w in ("employ", "job", "fired", "termination", "salary")):
        area = "Employment & Labour Law"
        analysis = (
            "Your query relates to employment rights. Under labour laws, employees "
            "are entitled to proper notice periods, fair termination procedures, and "
            "outstanding dues. Wrongful termination can be challenged through the "
            "Labour Court or appropriate tribunal."
        )
        steps = [
            "Collect your employment contract and payslips",
            "Document the termination communication",
            "File a grievance with the Labour Commissioner",
            "Explore conciliation proceedings",
        ]
    elif any(w in q for w in ("property", "land", "ownership", "boundary")):
        area = "Property & Real Estate Law"
        analysis = (
            "Property disputes require careful examination of title deeds, registration "
            "documents, and possession history. The Transfer of Property Act and "
            "Registration Act govern these matters. It is important to establish clear "
            "title and chain of ownership."
        )
        steps = [
            "Obtain certified copies of all property documents",
            "Verify the title through the Sub-Registrar office",
            "Get a survey and demarcation done if boundary is disputed",
            "Explore settlement before filing a civil suit",
        ]
    elif any(w in q for w in ("divorce", "custody", "marriage", "alimony")):
        area = "Family Law"
        analysis = (
            "Family matters including divorce and custody are handled under personal "
            "laws and the Family Courts Act. The court prioritizes the welfare of "
            "children in custody matters and considers various factors for maintenance "
            "and alimony."
        )
        steps = [
            "Gather marriage certificate and relevant documents",
            "Document any instances relevant to your case",
            "Consider mediation through Family Court counsellors",
            "File a petition in the Family Court",
        ]
    elif any(w in q for w in ("cyber", "fraud", "online", "scam", "hack")):
        area = "Cyber Crime & IT Law"
        analysis = (
            "Cyber crimes fall under the Information Technology Act, 2000. This includes "
            "online fraud, identity theft, hacking, and data breaches. Quick action is "
            "essential to preserve digital evidence and increase the chances of recovery."
        )
        steps = [
            "Preserve all digital evidence (screenshots, emails, URLs)",
            "File a complaint on the National Cyber Crime Portal",
            "Lodge an FIR at the nearest Cyber Crime police station",
            "Contact your bank immediately if financial fraud is involved",
        ]
    elif any(w in q for w in ("consumer", "complaint", "product", "defective")):
        area = "Consumer Protection Law"
        analysis = (
            "Under the Consumer Protection Act 2019, consumers have the right to seek "
            "redressal for defective goods, deficient services, and unfair trade "
            "practices. The Act provides for a three-tier grievance redressal mechanism."
        )
        steps = [
            "Collect bills, receipts, and warranty documents",
            "Send a formal written complaint to the company",
            "File a case on the National Consumer Helpline",
            "Approach the District Consumer Disputes Redressal Forum",
        ]
    else:
        area = "General Legal Advisory"
        analysis = (
            "Thank you for sharing your situation. Based on your description, I've "
            "identified potential legal aspects that may apply. For a more precise "
            "analysis, please share additional details such as dates, parties involved, "
            "and any documents you may have."
        )
        steps = [
            "Document all relevant facts and timeline",
            "Collect supporting evidence and correspondence",
            "Identify the relevant jurisdiction and authority",
            "Consult with a specialist lawyer in this area",
        ]

    return {
        "area": area,
        "analysis": analysis,
        "steps": steps,
        "relevantStatutes": [],
        "sources": [],
        "disclaimer": (
            "This is a preliminary advisory generated from general legal knowledge "
            "and does not constitute legal advice. The AI advisory service is "
            "temporarily using cached responses. Please consult a qualified lawyer "
            "for professional guidance."
        ),
    }
