# RAG AI Agent Backend

A minimal, production-ready FastAPI backend demonstrating **Retrieval-Augmented Generation (RAG)** with vector similarity search. Built for educational purposes and easy frontend integration.

## 🎯 Features

- **FastAPI** backend with automatic API documentation
- **Supabase** integration with pgvector for vector similarity search
- **Multi-AI Provider** support (OpenAI & Anthropic)
- **Vector embeddings** with semantic search
- **Citation-based answers** with source tracking
- **Frontend-ready** architecture for NextJS integration
- **Docker** containerization for easy deployment

## 🏗️ Architecture

```
Gary-Agent-RAG/
├── app/
│   ├── core/           # Infrastructure (config, database)
│   ├── models/         # Pydantic data models
│   ├── services/       # Business logic (RAG, embeddings)
│   └── main.py         # FastAPI application
├── sql/
│   └── init_supabase.sql  # Database initialization script
└── requirements.txt
```

## 🚀 Quick Start Guide

**Complete setup from clone to asking questions in ~10 minutes**

### Prerequisites

- Python 3.11+
- Supabase account
- OpenAI API key
- Anthropic API key (optional, for Claude)

### Step 1: Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/ZhaoYi-10-13/Gary-Agent-RAG.git
cd Gary-Agent-RAG

# Create virtual environment
python3.11 -m venv venv_gary_rag
source venv_gary_rag/bin/activate  # On Windows: venv_gary_rag\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get API Keys (5 minutes)

**Supabase Setup:**
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for project to be ready (~2 minutes)
3. Go to **Settings** → **API** and copy:
   - **Project URL** (e.g., `https://abc123.supabase.co`)
   - **Anon public key** (starts with `eyJ...`)
   - **Service role secret key** (starts with `eyJ...`)

**OpenAI Setup:**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create account/sign in → **API Keys** → Create new key
3. Copy the key (starts with `sk-...`)

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your real API keys
nano .env  # or use your preferred editor
```

**Update `.env` with your values:**
```env
# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# OpenAI Configuration (using latest models)
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_EMBED_MODEL=text-embedding-3-large
OPENAI_CHAT_MODEL=gpt-4o

# AI Provider
AI_PROVIDER=openai

# Optional: Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
ANTHROPIC_CHAT_MODEL=claude-3-5-sonnet-20241022
```

### Step 4: Initialize Database (2 minutes)

1. **Open Supabase Dashboard** → **SQL Editor**
2. **Click "New query"**
3. **Copy entire contents** of `sql/init_supabase.sql`
4. **Paste and click "Run"**

✅ This creates everything needed:
- pgvector extension
- `rag_chunks` table with VECTOR(3072) for latest embeddings
- Performance indexes
- Vector search functions
- RLS policies for future auth

### Step 5: Test Setup (Optional)

```bash
# Test your complete setup
python test_setup.py
```

This verifies:
- ✅ Dependencies installed
- ✅ API keys configured
- ✅ Database connected
- ✅ Schema initialized
- ✅ RAG pipeline working

### Step 6: Start the Server

```bash
uvicorn main:app --reload --port 8000
uvicorn main:app --host 0.0.0.0 --port 80 # For Aliyun service
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Usage

### Health Check
```bash
curl http://localhost:8000/healthz
```

### Seed Knowledge Base
```bash
# Seed with default documents
curl -X POST http://localhost:8000/seed

# Or seed with custom documents
curl -X POST http://localhost:8000/seed \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      {
        "chunk_id": "policy_returns_v1#window",
        "source": "https://help.example.com/returns",
        "text": "You can return unworn items within 30 days of purchase..."
      }
    ]
  }'
```

### Ask Questions (RAG)
```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Can I return shoes after 30 days?",
    "top_k": 6
  }'
```

**Example Response:**
```json
{
  "text": "Based on our return policy, you can return unworn shoes within 30 days of purchase [policy_returns_v1#window]. Items must be in original condition...",
  "citations": ["policy_returns_v1#window", "policy_returns_v1#conditions"],
  "debug": {
    "top_doc_ids": ["policy_returns_v1#window", "policy_returns_v1#conditions"],
    "latency_ms": 1250
  }
}
```

## 🔧 Configuration Options

### AI Providers

**OpenAI (Recommended)**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_EMBED_MODEL=text-embedding-3-small  # 1536 dimensions
OPENAI_CHAT_MODEL=gpt-4o-mini
```

**Anthropic Claude**
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key
ANTHROPIC_CHAT_MODEL=claude-3-haiku-20240307

# Note: Still need OpenAI key for embeddings
OPENAI_API_KEY=your_openai_key
```

### RAG Parameters

Adjust in `app/core/config.py`:
- `chunk_size`: Token limit per chunk (default: 400)
- `chunk_overlap`: Overlap between chunks (default: 60 tokens)
- `default_top_k`: Number of chunks to retrieve (default: 6)
- `temperature`: LLM creativity (default: 0.1)

## 🐳 Docker Deployment

```bash
# Build image
docker build -t yt-rag .

# Run container
docker run -p 8080:8080 --env-file .env yt-rag
```

## 🔮 NextJS Frontend Integration

This backend is designed for seamless frontend integration:

**Frontend Setup (NextJS)**
```javascript
// lib/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

// API calls to your backend
const response = await fetch('http://localhost:8000/answer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'user question' })
})
```

**Future Auth Integration**
When adding Google authentication:
1. Enable Google Auth in Supabase
2. The RLS policies are already configured
3. Frontend and backend will share the same Supabase client
4. No backend changes needed!

