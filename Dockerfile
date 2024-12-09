FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN set -x && \
    apt-get update && \
    apt-get install --no-install-recommends --assume-yes \
      build-essential \
    && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create user
ARG UID=1000
ARG GID=1000
RUN set -x && \
    groupadd -g "${GID}" python && \
    useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python &&\
    chown python:python -R /app

USER python

# Install python dependencies
COPY requirements.txt .
RUN  pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY src src

# don't buffer Python output
ENV PYTHONUNBUFFERED=1
# Add pip's user base to PATH
ENV PATH="$PATH:/home/python/.local/bin"

# expose port
EXPOSE 8080

CMD ["fastapi", "run", "src/main.py", "--port", "8080"]