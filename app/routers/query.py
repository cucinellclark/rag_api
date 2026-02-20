"""Query endpoints for document retrieval."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import get_config
from app.models.schemas import QueryRequest, QueryResponse, DocumentResult, ErrorResponse
from app.services.rag_service import get_rag_service

router = APIRouter(prefix="/query", tags=["query"])


@router.post(
    "/{database_name}",
    response_model=QueryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Database not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def query_database(database_name: str, request: QueryRequest) -> QueryResponse:
    """Query a RAG database for relevant documents.
    
    Args:
        database_name: Name of the RAG database to query.
        request: Query request containing the search query and parameters.
        
    Returns:
        QueryResponse with retrieved documents and query embedding.
    """
    try:
        print(f"[RAG API] checkpoint: request received for database='{database_name}'")
        config = get_config()
        rag_service = get_rag_service()
        top_k = request.top_k if request.top_k is not None else config.retrieval.default_top_k
        score_threshold = (
            request.score_threshold
            if request.score_threshold is not None
            else config.retrieval.default_score_threshold
        )
        print(
            f"[RAG API] checkpoint: starting search (top_k={top_k}, score_threshold={score_threshold})"
        )
        
        result = rag_service.search(
            db_name=database_name,
            query=request.query,
            top_k=top_k,
            score_threshold=score_threshold,
        )
        print("[RAG API] checkpoint: search finished")

        # Console logging of returned documents for operational visibility.
        returned_documents = result.get("documents", [])
        print(
            f"[RAG API] Query '{request.query[:80]}{'...' if len(request.query) > 80 else ''}' "
            f"returned {len(returned_documents)} document(s) from '{database_name}'"
        )
        for i, doc in enumerate(returned_documents, start=1):
            content = str(doc.get("content", "") or "")
            preview = content[:180].replace("\n", " ")
            if len(content) > 180:
                preview += "..."
            print(f"[RAG API] doc {i}: {preview}")
        
        documents = [
            DocumentResult(
                content=doc['content'],
                score=doc['score'],
                metadata=doc.get('metadata'),
            )
            for doc in result['documents']
        ]
        print(f"[RAG API] checkpoint: response ready (documents={len(documents)})")
        
        return QueryResponse(
            query=request.query,
            database=database_name,
            documents=documents,
            embedding=result.get('embedding'),
            total_results=len(documents),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

