FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim

RUN apt-get update && apt-get install -y \
    git \
    vim \
    gcc \
    procps\
    python3-dev \
    && apt-get clean \  
    && rm -rf /var/lib/apt/lists/* 


# 代码挂载点
WORKDIR /app


COPY requirements.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade pip  && \
    pip install --no-cache-dir -r requirements.txt