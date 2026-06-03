# CloneMe 2.0 - RAG System Documentation

## Overview

The Retrieval-Augmented Generation (RAG) system allows CloneMe to retrieve and inject relevant document excerpts into the AI response pipeline, enabling more accurate and context-aware responses based on uploaded training documents.

## Architecture

### Components

1. **Embedding Service** (`app/services/embeddings.py`)
   - Generates embeddings using sentence-transformers (`all-MiniLM-L6-v2`)
   - Computes cosine similarity between vectors
   - Fallback support if embedding model unavailable

2. **Document Processor** (`app/services/document_processor.py`)
   - Chunks documents into fixed-size pieces (500 chars, 100 char overlap)
   - Generates embeddings for each chunk
   - Stores chunks with embeddings in MongoDB

3. **Retrieval Service** (`app/services/retrieval.py`)
   - Generates query embedding from user message
   - Performs semantic search via cosine similarity
   - Returns top-k most relevant chunks (threshold: 0.25 by default)
   - Supports filtering by document

4. **Context Builder** (`app/services/context_builder.py`)
   - Orchestrates all context sources
   - Automatically retrieves relevant chunks via RAG
   - Builds final enriched prompt for LLM

5. **Document Chunk Model** (`app/models/document_chunk.py`)
   - Stores chunk text, embedding vector, and metadata
   - Links to source document

## Data Flow

```
User uploads document
  ↓
Document stored in training_documents collection
  ↓
User triggers process endpoint
  ↓
Document Processor chunks the text
  ↓
Embedding Service generates embeddings for each chunk
  ↓
Chunks stored in document_chunks collection with embeddings
  ↓
User asks a question
  ↓
Query embedding generated
  ↓
Retrieval Service finds top-5 similar chunks
  ↓
Chunks injected into context before LLM prompt
  ↓
LLM generates response with RAG context
```

## API Endpoints

### Document Management

**Upload Document**
```
POST /api/training/upload
Headers: Authorization: Bearer <token>
Body: {
  "title": "My Resume",
  "document_type": "resume",
  "content": "...",
  "tags": ["career", "experience"]
}
Response: {
  "success": true,
  "message": "Document uploaded",
  "data": {"document_id": "..."}
}
```

**List Documents**
```
GET /api/training/list
Headers: Authorization: Bearer <token>
Response: {
  "success": true,
  "data": [
    {
      "id": "...",
      "title": "My Resume",
      "document_type": "resume",
      "processed": false,
      "chunk_count": 0,
      "created_at": "..."
    }
  ]
}
```

**Process Document (Generate Embeddings)**
```
POST /api/training/process
Headers: Authorization: Bearer <token>
Body: {
  "document_id": "..."
}
Response: {
  "success": true,
  "message": "Document processed with RAG",
  "data": {
    "document_id": "...",
    "chunks_created": 12
  }
}
```

**Delete Document**
```
DELETE /api/training/<document_id>
Headers: Authorization: Bearer <token>
Response: {
  "success": true,
  "message": "Document deleted"
}
```

**Train Clone (Get Stats)**
```
POST /api/training/train
Headers: Authorization: Bearer <token>
Response: {
  "success": true,
  "message": "Clone training initiated",
  "data": {
    "processed_documents": 5,
    "total_chunks": 87
  }
}
```

## Clone Response Pipeline

When user sends a query to `/api/clone/respond`:

1. **Personality Profile** loaded from DB
2. **Memories** retrieved (last 10)
3. **Training Documents** loaded (summary)
4. **Future Profile** loaded
5. **Conversation History** retrieved (last 4)
6. **RAG Retrieval** automatically finds top-5 relevant chunks
7. **Context Built** with all sources
8. **Prompt Generated** with RAG context injected
9. **LLM Response** generated with enriched context
10. **Conversation Recorded** with metadata

Example request:
```json
{
  "prompt": "What projects should I highlight in interviews?",
  "mode": "interview"
}
```

The system will:
- Embed the query
- Find relevant project excerpts from uploaded documents
- Inject them into the response context
- Generate personalized advice based on the user's actual projects

## MongoDB Collections

### training_documents
```javascript
{
  "_id": ObjectId,
  "user_id": "...",
  "title": "My Resume",
  "document_type": "resume|portfolio|project|notes",
  "content": "...",
  "source": "upload",
  "processed": true,
  "chunk_count": 12,
  "summary": "...",
  "tags": ["career"],
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### document_chunks
```javascript
{
  "_id": ObjectId,
  "user_id": "...",
  "document_id": "...",
  "chunk_index": 0,
  "chunk_text": "...",
  "embedding": [0.123, -0.456, ...],
  "metadata": {
    "title": "My Resume",
    "document_type": "resume"
  },
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## Configuration

Update `.env`:
```
EMBEDDING_MODEL=all-MiniLM-L6-v2
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=100
RAG_SIMILARITY_THRESHOLD=0.25
RAG_RETRIEVE_LIMIT=5
```

## Performance Notes

- Embeddings are generated using `sentence-transformers` (fast, lightweight)
- Chunk size optimized for semantic coherence (500 chars)
- Cosine similarity computed in-memory
- Consider indexing on `user_id` and `document_id` for scale
- Context window limited to 3000 chars to prevent LLM overload

## Error Handling

- Missing documents return 404
- Invalid ObjectId returns 400
- Processing without embeddings falls back gracefully
- No chunks retrieved returns empty RAG section

## Next Steps

1. Implement MongoDB vector index for faster retrieval
2. Add support for PDF/document parsing
3. Implement chunk reranking
4. Add query expansion for better retrieval
5. Support for multi-language embeddings
