# Build from the repository root so the legal corpus (frontend/data, frontend/pakistan_legal_corpus) is in context:
#   docker build -f backend/Dockerfile -t pjn-backend .
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    HF_HUB_DISABLE_SYMLINKS_WARNING=1 \
    ENVIRONMENT=production LEGAL_DATA_DIR=/srv/legal SQLITE_PATH=/srv/state/pjn.sqlite3 UPLOAD_DIR=/srv/state/uploads

WORKDIR /srv/app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/app ./app
COPY backend/scripts ./scripts
COPY backend/eval ./eval
COPY frontend/data /srv/legal/data
COPY frontend/pakistan_legal_corpus /srv/legal/pakistan_legal_corpus

# Bake the embedding model into the image so cold starts do not download it.
RUN python -c "from app.legal.embeddings import FastEmbedEmbedder; FastEmbedEmbedder().embed(['warmup'])"

RUN useradd --system --uid 10001 pjn && mkdir -p /srv/state && chown -R pjn /srv/state /srv/app/.cache 2>/dev/null || true
USER pjn
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status==200 else 1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers"]
