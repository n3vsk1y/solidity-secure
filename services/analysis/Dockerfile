FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir solc-select

RUN solc-select install 0.8.20 && solc-select use 0.8.20

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
