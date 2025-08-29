# 代码界面渲染

## 1. 修改配置文件

服务依赖代码模型生成对应的前端代码，并且依赖 selenium/standalone-chrome 镜像作为浏览器访问代理，提供的 selenium+webdriver+headless 浏览器的截屏功能。

### 1.1 模型配置
基于调用模型，修改 **config/config_prod.yaml** 当中对应OpenAI的相关配置

``` yaml
# openai config
base_url: http://localhost:8001/v1    
api_key: sk-XXXXXX         
model: Qwen3
```

### 1.2 服务内部线程池大小
线程池大小决定服务内部同一时间能够处理的最大任务数量。比如同一个时间收到10个api请求，每个请求内部包括15个图片生成需求，则此时并发应当对应150个任务处理线程。

根据业务需求修改**config/base.yaml** 当中的线程配置：

``` yaml
# service config
max_workers: 150          # multithread
```

### 1.3 Chrome Driver的sessions数量
对于每一张图片均需要单独在Selenium中初始化一个Chrome Driver，对应于启动一个浏览器渲染代码。每个浏览器进程（如 Chrome）启动后约占用 200-500MB 内存。因此单结点的承载driver数量受限于server的内存和CPU核心数量。即虽然配置了线程池，但是线程之间仍然会争抢配置的有限个Driver。

根据业务需求，修改 **docker-compose.yml** 中的Seleium配置：

``` yml
  # Selenium Chrome Image
  leixin-chrome:
    image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/selenium/standalone-chrome:latest
    container_name: leixin-selenium-chrome
    shm_size: 8g                       # default 8G shared memory
    network_mode: host
    environment:
      - SE_NODE_MAX_SESSIONS=15        # default 15 sessions
      - SE_NODE_SESSION_TIMEOUT=120
```




## 2. 服务接口

当前服务对外提供两个接口：

- /v1/gen_images
- /v1/progress/{request_id}

具体的接口请参考 [接口文档](docs/接口文档.md)

### 2.1 生成请求
``` bash
# 发送请求
curl -X POST http://localhost:8687/v1/gen_images -H "Content-Type: application/json"  -d @docs/测试输入.json
```

此时会立马返回对应的任务ID号，如下所示。其中 **request_id** 为系统自动为本次请求创建的唯一ID，后续可基于此ID查询任务进度。

``` bash
{"code":0,"message":"任务创建成功!","request_id":"d0793ba1-32df-44f1-b5fb-6dbd4ec211a5","task_id":"20250813104545707549754_TASK_REPORT"}
```

### 2.2 查询进度
根据返回的 **request_id**，继续根据这个任务ID号查询状态。

```bash
# 获取处理状态
curl http://localhost:8687/v1/progress/<request_id>
```


## 3. 服务启动

### 3.1 Flask测试服务器
直接使用Flask作为测试服务器开发API服务，方便开发
``` bash
python wsgi.py
```

### 3.2 uWSGI服务器
使用uwsgi 提供接口服务
``` bash
# 启动
uwsgi --ini uwsgi_service.ini

# 停止
uwsgi --stop log/uwsgi.pid
```


## 4. Docker 启动
项目提供 docker-compose.yml 方便同时管理项目的环境镜像和Chrome镜像，环境镜像需要实现打包，业务代码通过映射到镜像中的 */app* 文件目录。

### 4.1 创建环境镜像
```bash
# 创建镜像，不含业务代码
docker compose build
```

### 4.2 服务启动

``` bash
# 启动服务
docker compose up -d

# 查看容器状态（此时依赖的两个容器应当均为 running）
docker compose ps

# 进入容器
docker compose exec leixin-coder-artifacts bash

# 服务启动
uwsgi --ini uwsgi_service.ini
```

### 4.3 服务停止
``` bash
# 停止容器
docker compose down
```

## 5. 项目结构

```
coder-artifacts
├─ Dockerfile
├─ README.md
├─ config
│  ├─ base.yaml            # 基础配置  
│  └─ config_prod.yaml     # 服务配置
├─ docker-compose.yml
├─ docs
│  ├─ 接口文档.md
│  ├─ 测试输入.json
│  └─ 测试返回.json
├─ requirements.txt
├─ src
│  ├─ api
│  │  ├─ __init__.py
│  │  └─ routes.py       # API
│  ├─ app.py             # Flask app初始化
│  ├─ browser
│  │  ├─ __init__.py
│  │  ├─ manager.py      # Selenium Driver相关
│  │  └─ renderer.py     # Gradio界面渲染相关
│  ├─ config
│  │  ├─ __init__.py
│  │  └─ loader.py       # 配置文件加载
│  ├─ core
│  │  ├─ data_processing    # JSON解析处理 / 模板控制
│  │  │  ├─ __init__.py
│  │  │  ├─ json_parser.py
│  │  │  └─ tmpl_manager.py
│  │  ├─ progress            # 流程控制，处理状态JSON
│  │  │  ├─ __init__.py
│  │  │  └─ progress_store.py
│  │  ├─ storage             # 存储管理，DFS与本地文件
│  │  │  ├─ __init__.py
│  │  │  ├─ dfs_upload.py
│  │  │  └─ local_storage.py
│  │  └─ task_manager.py    # 任务核心，负责拆解与执行任务
│  ├─ db
│  │  ├─ __init__.py
│  │  └─ client.py       # MongoDB 相关
│  ├─ errors.py
│  ├─ llm
│  │  ├─ __init__.py
│  │  ├─ client.py       # LLM 相关
│  │  └─ prompt.py
│  └─ utils
│     ├─ __init__.py
│     ├─ common.py
│     └─ logger.py
├─ static                # 不同局部的静态jsx模板
│  ├─ 上中下布局
│  ├─ 侧边布局
│  ├─ 小程序
│  └─ 顶部-侧边布局
├─ uwsgi_service.ini     # uwsgi 配置文件
└─ wsgi.py               # 服务入口

```