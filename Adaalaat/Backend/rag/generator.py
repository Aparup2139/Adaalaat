"""
RAG Pipeline — Generator Module

Uses an LLM to synthesize responses from the query + retrieved context.
Now wired to use the custom HuggingFace Inference LLM.
"""

import json
from rag.hf_inference_llm import HFInferenceLLM
from llama_index.core.llms import ChatMessage

# Initialize our custom LLM (it automatically reads the .env token)
llm = HFInferenceLLM()

def generate_advisory(query, context_docs):
    """
    Generate a preliminary legal advisory report.
    """
    # Extract text from the retrieved context dictionaries
    if not context_docs:
        context_text = "No relevant legal documents were found."
    elif isinstance(context_docs[0], dict):
        context_text = "\n\n".join([doc.get("text", "") for doc in context_docs])
    else:
        # Fallback if context_docs is just a list of strings
        context_text = "\n\n".join(context_docs)
    
    system_prompt = (
        "You are a legal advisory AI specializing in Indian law. "
        "Analyze the user's situation using the provided legal context. "
        "Respond strictly with a valid JSON object containing: "
        '"area" (string, the legal domain), '
        '"analysis" (string, detailed analysis), '
        '"steps" (list of strings, recommended next steps), '
        '"relevantStatutes" (list of strings, applicable laws/sections).'
    )
    
    user_prompt = f"Legal Context:\n{context_text}\n\nClient Query:\n{query}"

    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt)
    ]

    try:
        # Call the HuggingFace LLM
        response = llm.chat(messages)
        raw_content = response.message.content.strip()
        
        # Clean up the output in case the LLM wrapped it in markdown code blocks
        if "```" in raw_content:
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"):
                raw_content = raw_content[4:]
            raw_content = raw_content.strip()

        return json.loads(raw_content)
    except Exception as e:
        print(f"Error generating advisory: {e}")
        return {
            "area": "Error",
            "analysis": "Could not generate analysis due to an API error.",
            "steps": [],
            "relevantStatutes": []
        }

def generate_document_draft(document_type, context, reference_docs):
    """
    Generate a legal document draft using retrieved templates.
    """
    # This follows the exact same pattern as above, but with a drafting prompt.
    context_text = "\n\n".join([doc.get("text", "") for doc in reference_docs])
    
    system_prompt = (
        f"You are an expert legal drafter. Draft a '{document_type}' based on the user's context "
        "and the provided reference templates. "
        "Respond strictly with a JSON object containing: "
        '"title" (string), "content" (string, the full draft).'
    )
    
    user_prompt = f"Reference Templates:\n{context_text}\n\nClient Context:\n{context}"

    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt)
    ]

    try:
        response = llm.chat(messages)
        raw_content = response.message.content.strip()
        
        if "```" in raw_content:
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"):
                raw_content = raw_content[4:]
            raw_content = raw_content.strip()

        return json.loads(raw_content)
    except Exception as e:
        return {"title": "Error", "content": f"Failed to draft document: {e}"}