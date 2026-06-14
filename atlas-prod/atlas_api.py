"""
ATLAS AI — FastAPI backend
"""

import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")

vectorstore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore
    embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embed_model)
    yield


app = FastAPI(title="ATLAS AI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SourceDoc(BaseModel):
    source: str
    snippet: str


class AskRequest(BaseModel):
    query: str
    model: str = "claude-sonnet-4-6"
    temperature: float = 0.0
    top_k: int = 5
    api_key: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceDoc]


@app.get("/health")
def health():
    return {"status": "ok", "chroma_dir": CHROMA_DIR}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if vectorstore is None:
        raise HTTPException(status_code=503, detail="Vectorstore not ready")

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    api_key = request.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="No Anthropic API key provided")

    retriever = vectorstore.as_retriever(search_kwargs={"k": request.top_k})
    docs = retriever.invoke(request.query)
    context = "\n\n".join(d.page_content for d in docs)

    llm = ChatAnthropic(
        model=request.model,
        temperature=request.temperature,
        api_key=api_key,
    )
    prompt = f"Context:\n{context}\n\nQuestion: {request.query}"
    result = llm.invoke(prompt)
    answer = result.content if isinstance(result.content, str) else str(result.content)

    sources = [
        SourceDoc(
            source=d.metadata.get("source", "unknown"),
            snippet=d.page_content[:220].replace("\n", " "),
        )
        for d in docs
    ]

    return AskResponse(answer=answer, sources=sources)
