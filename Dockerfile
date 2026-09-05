FROM python:3.12.13-slim-bookworm@sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2

RUN groupadd --gid 10001 biomune \
    && useradd --uid 10001 --gid biomune --no-create-home --shell /usr/sbin/nologin biomune

WORKDIR /app
COPY --chown=biomune:biomune server.py /app/server.py

USER biomune
EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:10000/healthz', timeout=2)"]

CMD ["python", "/app/server.py"]
