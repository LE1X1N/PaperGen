FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim

RUN rm -rf /etc/apt/sources.list /etc/apt/sources.list.d/* && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ bookworm-security main contrib non-free" >> /etc/apt/sources.list 
    
RUN apt-get update && \
    apt-get install -y \
        dbus \
        git \
        vim \
        gcc \
        curl \
        procps \
        python3-dev && \
    apt-get clean && \ 
    rm -rf /var/lib/apt/lists/* 

WORKDIR /app

COPY requirements.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade pip  && \
    pip install --no-cache-dir -r requirements.txt
