-- ============ RESET & RECREATE (1024-d) ============
-- 0) Extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 1) Drop dependent objects
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='public' AND p.proname='match_chunks'
               AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1536), match_count integer, min_similarity double precision') THEN
    EXECUTE 'DROP FUNCTION public.match_chunks(vector(1536), int, float)';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='public' AND p.proname='match_chunks'
               AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1536), match_threshold double precision, match_count integer, min_content_length integer') THEN
    EXECUTE 'DROP FUNCTION public.match_chunks(vector(1536), float, int, int)';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='public' AND p.proname='match_chunks'
               AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1024), match_count integer, min_similarity double precision') THEN
    EXECUTE 'DROP FUNCTION public.match_chunks(vector(1024), int, float)';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='public' AND p.proname='match_chunks'
               AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1024), match_threshold double precision, match_count integer, min_content_length integer') THEN
    EXECUTE 'DROP FUNCTION public.match_chunks(vector(1024), float, int, int)';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='public' AND p.proname='get_chunk_stats') THEN
    EXECUTE 'DROP FUNCTION public.get_chunk_stats()';
  END IF;
END$$;

-- 2) Drop policies & indexes & table
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='rag_chunks') THEN
    EXECUTE 'ALTER TABLE public.rag_chunks DISABLE ROW LEVEL SECURITY';
    EXECUTE 'DROP POLICY IF EXISTS "Allow service role full access"  ON public.rag_chunks';
    EXECUTE 'DROP POLICY IF EXISTS "Allow authenticated read access" ON public.rag_chunks';
    EXECUTE 'DROP POLICY IF EXISTS "Allow anonymous read access"     ON public.rag_chunks';
    EXECUTE 'DROP INDEX  IF EXISTS public.rag_chunks_vec_idx';
    EXECUTE 'DROP INDEX  IF EXISTS public.rag_chunks_src_idx';
    EXECUTE 'DROP INDEX  IF EXISTS public.rag_chunks_chunk_id_idx';
    EXECUTE 'DROP INDEX  IF EXISTS public.rag_chunks_created_at_idx';
    EXECUTE 'DROP TABLE  IF EXISTS public.rag_chunks CASCADE';
  END IF;
END$$;

-- 3) Recreate table (1024-d)
CREATE TABLE public.rag_chunks (
  id         BIGSERIAL PRIMARY KEY,
  chunk_id   TEXT NOT NULL UNIQUE,
  source     TEXT NOT NULL,
  text       TEXT NOT NULL,
  embedding  VECTOR(1024),              
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 4) Indexes
CREATE INDEX rag_chunks_vec_idx
  ON public.rag_chunks
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX rag_chunks_src_idx        ON public.rag_chunks (source);
CREATE INDEX rag_chunks_chunk_id_idx   ON public.rag_chunks (chunk_id);
CREATE INDEX rag_chunks_created_at_idx ON public.rag_chunks (created_at DESC);

-- 5) RPC
-- 5.1 match_count + min_similarity
CREATE OR REPLACE FUNCTION public.match_chunks (
  query_embedding vector(1024),
  match_count     int   DEFAULT 6,
  min_similarity  float DEFAULT 0.0
)
RETURNS TABLE (
  chunk_id   text,
  source     text,
  text       text,
  similarity float,
  created_at timestamptz
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
  RETURN QUERY
  SELECT
    rc.chunk_id,
    rc.source,
    rc.text,
    1 - (rc.embedding <=> query_embedding) AS similarity,
    rc.created_at
  FROM public.rag_chunks rc
  WHERE 1 - (rc.embedding <=> query_embedding) >= min_similarity
  ORDER BY rc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- 5.2 threshold + count + min_content_length
CREATE OR REPLACE FUNCTION public.match_chunks (
  query_embedding    vector(1024),
  match_threshold    float,
  match_count        int,
  min_content_length int
)
RETURNS TABLE (
  chunk_id   text,
  source     text,
  text       text,
  similarity float,
  created_at timestamptz
)
LANGUAGE sql
STABLE
AS $$
  SELECT
    rc.chunk_id,
    rc.source,
    rc.text,
    1 - (rc.embedding <=> query_embedding)::float AS similarity,
    rc.created_at
  FROM public.rag_chunks rc
  WHERE length(rc.text) >= min_content_length
    AND 1 - (rc.embedding <=> query_embedding) >= match_threshold
  ORDER BY rc.embedding <-> query_embedding
  LIMIT match_count
$$;

-- 6) Stats function
CREATE OR REPLACE FUNCTION public.get_chunk_stats()
RETURNS TABLE (
  total_chunks   bigint,
  unique_sources bigint,
  latest_chunk   timestamptz
)
LANGUAGE sql
STABLE
AS $$
  SELECT
    COUNT(*)::bigint,
    COUNT(DISTINCT source)::bigint,
    MAX(created_at)
  FROM public.rag_chunks
$$;

-- 7) RLS & policies
ALTER TABLE public.rag_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow service role full access" ON public.rag_chunks
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Allow authenticated read access" ON public.rag_chunks
  FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Allow anonymous read access" ON public.rag_chunks
  FOR SELECT USING (true);

GRANT EXECUTE ON FUNCTION public.match_chunks(vector(1024), int, float)   TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.match_chunks(vector(1024), float, int, int) TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.get_chunk_stats()                         TO anon, authenticated, service_role;

-- 8) Verification
SELECT 'pgvector OK' AS test_result
WHERE EXISTS (SELECT 1 FROM pg_extension WHERE extname='vector');

SELECT 'rag_chunks OK' AS test_result
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='rag_chunks');

SELECT 'embedding VECTOR(1024) OK' AS test_result
WHERE EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rag_chunks' AND column_name='embedding');

SELECT 'match_chunks 3-args OK' AS test_result
WHERE EXISTS (
  SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
  WHERE n.nspname='public' AND p.proname='match_chunks'
    AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1024), match_count integer, min_similarity double precision'
);

SELECT 'match_chunks 4-args OK' AS test_result
WHERE EXISTS (
  SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
  WHERE n.nspname='public' AND p.proname='match_chunks'
    AND pg_get_function_identity_arguments(p.oid) LIKE 'query_embedding vector(1024), match_threshold double precision, match_count integer, min_content_length integer'
);

SELECT 'get_chunk_stats OK' AS test_result
WHERE EXISTS (
  SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
  WHERE n.nspname='public' AND p.proname='get_chunk_stats'
);

SELECT 'Database ready - ' || total_chunks::text || ' chunks' AS test_result
FROM public.get_chunk_stats();

-- 初次大量导入后建议
-- ANALYZE public.rag_chunks;
