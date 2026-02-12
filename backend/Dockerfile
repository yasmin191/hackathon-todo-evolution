# Backend Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src

# Install dependencies
RUN uv sync --no-dev

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Expose port (7860 for Hugging Face Spaces)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

# Start server
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
