#!/usr/bin/env python3
# Copyright 2024
# Directory: yt-rag/test_setup.py

"""
Test script to verify RAG backend setup is working correctly.
Run this after completing the setup steps.

改动要点：
1) 在导入项目模块前，清理掉 OPENAI_API_BASE 等非法 key（避免 Pydantic extra=forbid）
2) 按 AI_PROVIDER 动态校验所需的环境变量（aliyun / openai）
3) 按 provider 打印 Chat / Embedding 实际配置与 Base URL
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))


def _sanitize_env():
    """清理 Pydantic 不允许的 env 键"""
    forbidden = ["OPENAI_API_BASE", "OPENAI_BASE_URL", "openai_api_base", "openai_base_url"]
    removed = []
    for key in forbidden:
        if key in os.environ:
            removed.append((key, os.environ.pop(key)))
    if removed:
        print("ℹ️  Removed unsupported keys for Pydantic(extra='forbid'):")
        for k, _ in removed:
            print(f"   - {k} (was set)")


async def test_setup():
    """Test the complete RAG setup."""
    print("🧪 Testing RAG Backend Setup...")
    print("=" * 50)

    try:
        # Test 1: Import modules
        print("1️⃣  Testing imports...")
        from app.core.config import get_settings
        from app.core.database import db
        from app.services.rag import rag_service
        print("   ✅ All modules imported successfully")

        # Test 2: Check configuration
        print("\n2️⃣  Testing configuration...")
        settings = get_settings()
        provider = (getattr(settings, "ai_provider", "aliyun") or "aliyun").lower()

        # 基础必需项（与 provider 无关）
        required_vars = [
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY",
            "SUPABASE_SERVICE_ROLE_KEY",
        ]
        # 根据 provider 追加必需项
        if provider == "aliyun":
            required_vars += ["ALIYUN_API_KEY"]
        else:
            required_vars += ["OPENAI_API_KEY"]

        missing = [v for v in required_vars if not os.getenv(v) or "your_" in os.getenv(v)]
        if missing:
            print(f"   ❌ Missing environment variables: {', '.join(missing)}")
            return False

        # 打印关键配置（随 provider 变化）
        print("   ✅ Environment variables configured")
        if provider == "aliyun":
            print(f"   📊 Embedding model: {getattr(settings, 'aliyun_embed_model', 'N/A')}")
            print(f"   🤖 Chat model: {getattr(settings, 'aliyun_chat_model', 'N/A')}")
            print(f"   🔗 AI provider: {provider}")
            print(f"   🌐 Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1")
        else:
            print(f"   📊 Embedding model: {getattr(settings, 'openai_embed_model', 'N/A')}")
            print(f"   🤖 Chat model: {getattr(settings, 'openai_chat_model', 'N/A')}")
            print(f"   🔗 AI provider: {provider}")
            # OpenAI 情况不强制打印 base_url，避免误导

        # Test 3: Database connection
        print("\n3️⃣  Testing database connection...")
        await db.connect()
        if not await db.health_check():
            print("   ❌ Database connection failed")
            return False
        print("   ✅ Database connection successful")

        # Test 4: Schema validation
        print("\n4️⃣  Testing database schema...")
        await db.initialize_schema()
        print("   ✅ Database schema validated")

        # Test 5: Seeding documents
        print("\n5️⃣  Testing document seeding...")
        inserted = await rag_service.seed_documents()
        if inserted == 0:
            print("   ⚠️  No new documents inserted (may already exist)")
        else:
            print(f"   ✅ Seeded {inserted} document chunks")

        # Test 6: RAG query
        print("\n6️⃣  Testing RAG query...")
        result = await rag_service.answer_query("Can I return shoes after 30 days?")
        txt = result.get("text")
        if not txt or "error" in str(txt).lower():
            print("   ❌ RAG query failed")
            print(f"   🔍 Response: {txt}")
            return False

        print("   ✅ RAG query successful!")
        print(f"   📝 Answer: {txt[:100]}...")
        print(f"   📚 Citations: {result.get('citations')}")
        if "debug" in result:
            print(f"   ⏱️  Latency: {result['debug'].get('latency_ms', 'N/A')}ms")

        await db.disconnect()
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"   ❌ Setup test failed: {e}")
        return False


async def main():
    print("🔧 RAG Backend Setup Verification")
    print("This will test your complete setup without starting the server.\n")

    from dotenv import load_dotenv
    load_dotenv()
    _sanitize_env()

    ok = await test_setup()
    if ok:
        print("\n🎯 Next Steps:")
        print("1. Start the server: uvicorn main:app --reload --port 8000")
        print("2. Test the health endpoint: curl http://localhost:8000/healthz")
        print("3. Ask a question: curl -X POST http://localhost:8000/answer -H 'Content-Type: application/json' -d '{\"query\":\"What is your return policy?\"}'")
        print("4. Visit docs: http://localhost:8000/docs")
        sys.exit(0)
    else:
        print("\n❌ Setup incomplete. Please fix and retry.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
