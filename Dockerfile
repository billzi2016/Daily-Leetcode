FROM python:3.12-slim

WORKDIR /app

# Install git (required for committer.py)
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configure git identity inside container
RUN git config --global user.email "leetcode@daily.local" \
    && git config --global user.name "Daily LeetCode"

# Point Ollama at the host machine
# ENV OLLAMA_URL=http://host.docker.internal:11434/api/generate
ENV OLLAMA_URL=http://10.54.79.119:11434/api/generate

CMD ["python", "main.py", "--all"]
