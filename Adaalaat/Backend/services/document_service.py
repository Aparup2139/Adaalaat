"""
Document Service
Handles RAG-based document drafting, listing, and sending.
"""

from database.supabase_client import get_supabase_client
from rag.retriever import retrieve_relevant_docs
from rag.embeddings import embed_query
from rag.generator import generate_document_draft


class DocumentService:

    @staticmethod
    def generate_draft(case_id, lawyer_id, document_type, context):
        """
        Generate a legal document draft using RAG.

        Pipeline:
            1. Embed the context + document type into a query vector
            2. Retrieve relevant document templates from Qdrant
            3. LLM generates a tailored draft
            4. Store draft metadata in Supabase

        Args:
            case_id: Optional case reference
            lawyer_id: The lawyer requesting the draft
            document_type: Type of document (Legal Notice, Appeal Letter, etc.)
            context: Description of what the document should address

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            # Step 1: Build a search query combining type and context
            search_query = f"{document_type}: {context}"
            query_vector = embed_query(search_query)

            # Step 2: Retrieve relevant templates/sections
            retrieved_docs = retrieve_relevant_docs(query_vector, top_k=3)

            # Step 3: Generate draft via LLM
            draft = generate_document_draft(
                document_type=document_type,
                context=context,
                reference_docs=retrieved_docs,
            )

            # Step 4: Store in Supabase
            supabase = get_supabase_client()
            doc_record = {
                "case_id": case_id,
                "lawyer_id": lawyer_id,
                "title": draft.get("title", f"{document_type} Draft"),
                "content": draft.get("content", ""),
                "document_type": document_type,
                "status": "draft",
            }
            response = supabase.table("documents").insert(doc_record).execute()
            saved = response.data[0] if response.data else doc_record

            return {
                "documentId": saved.get("id"),
                "title": saved.get("title"),
                "content": saved.get("content"),
                "documentType": saved.get("document_type"),
                "status": "draft",
                "createdAt": saved.get("created_at"),
            }, None

        except Exception as e:
            return None, f"Draft generation failed: {str(e)}"

    @staticmethod
    def list_documents(user_id, role="", status=""):
        """
        List documents for a user.

        Args:
            user_id: The user's ID
            role: "client" or "lawyer" — determines which column to filter
            status: Optional status filter

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            id_column = "lawyer_id" if role == "lawyer" else "client_id"
            query = (
                supabase.table("documents")
                .select("*", count="exact")
                .eq(id_column, user_id)
            )

            if status:
                query = query.eq("status", status)

            query = query.order("created_at", desc=True)
            response = query.execute()

            documents = []
            for row in response.data:
                documents.append({
                    "id": row["id"],
                    "title": row.get("title", ""),
                    "type": row.get("document_type", ""),
                    "status": row.get("status", ""),
                    "date": row.get("created_at", ""),
                })

            return {
                "documents": documents,
                "total": response.count or len(documents),
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def send_document(doc_id, lawyer_id, client_id, notes=""):
        """
        Mark a document as sent from lawyer to client.

        Updates the document status and records the delivery in Supabase.

        Args:
            doc_id: The document's ID
            lawyer_id: Sending lawyer's ID
            client_id: Receiving client's ID
            notes: Optional message to the client

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            # Update document status to 'sent' and assign client
            supabase.table("documents").update({
                "status": "sent",
                "client_id": client_id,
                "notes": notes,
            }).eq("id", doc_id).eq("lawyer_id", lawyer_id).execute()

            return {"documentId": doc_id}, None

        except Exception as e:
            return None, str(e)
