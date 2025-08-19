# 代码界面渲染

## 1. 项目结构

```
coder-artifacts
├─ Dockerfile
├─ README.md
├─ config
│  ├─ config.yaml            # 服务配置
├─ docs
│  ├─ 接口文档.md
│  ├─ 测试输入.json
│  └─ 测试返回.json
├─ requirements.txt
├─ src
│  ├─ api
│  │  ├─ __init__.py
│  │  └─ routes.py          # API
│  ├─ app.py                # Flask app初始化
│  ├─ browser
│  │  ├─ __init__.py
│  │  ├─ manager.py         # Selenium Driver相关
│  │  └─ renderer.py        # Gradio界面渲染相关
│  ├─ config
│  │  ├─ __init__.py
│  │  └─ loader.py
│  ├─ core
│  │  ├─ data_parser.py        # JSON解析处理
│  │  ├─ progress_manager.py   # 流程控制，读写结果
│  │  ├─ task_manager.py       # 请求任务分解与处理核心
│  │  ├─ tmpl_manager.py       # 管理静态jsx模板
│  │  └─ upload_manager.py     # 负责上传文件
│  ├─ errors.py  
│  ├─ llm
│  │  ├─ __init__.py
│  │  └─ client.py             # LLM调用
│  └─ utils 
│     ├─ __init__.py
│     ├─ common.py
│     └─ logger.py
├─ static                      # 不同局部的静态jsx模板
│  ├─ 上中下布局
│  ├─ 侧边布局
│  ├─ 小程序
│  └─ 顶部-侧边布局
├─ uwsgi_service.ini           # uwsgi 配置文件
└─ wsgi.py                     # 服务入口

```


## 2. 代码模型和Chrome启动

服务依赖代码模型生成对应的前端代码，并且依赖 selenium/standalone-chrome 镜像作为浏览器访问代理，提供的 selenium+webdriver+headless 浏览器的截屏功能。

### 2.1 代码模型启动 （可选）

``` bash
# 本地启动
CUDA_VISIBLE_DEVICES=2,3 vllm serve ~/huggingface/Qwen3-Coder-30B-A3B-Instruct/  --port 8001  --gpu-memory-utilization 0.90  --served-model-name Qwen3 --enable_chunked_prefill --enable_prefix_caching
```

需要同步修改 **config/config.yaml** 当中对应OpenAI的相关配置
``` yaml
# openai config
base_url: http://localhost:8001/v1    
api_key: sk-XXXXXX         
model: Qwen3
```

### 2.2 Selenium容器启动
``` bash
# 启动
docker run -d --network host --name leixin-selenium-chrome selenium/standalone-chrome

# 停止 
docker stop selenium-chrome
docker rm selenium-chrome
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

## 3.3 服务测试

当前服务对外提供两个接口：

- /v1/gen_images
- /v1/progress/{request_id}

具体的接口请参考 [接口文档](docs/接口文档.md)

### 3.3.1 生成请求
``` bash
# 发送请求
curl -X POST http://localhost:8687/v1/gen_images -H "Content-Type: application/json"  -d @docs/测试输入.json
```

此时会立马返回对应的任务ID号，如下所示。其中 **request_id** 为系统自动为本次请求创建的唯一ID，后续可基于此ID查询任务进度。

``` bash
{"code":0,"message":"任务创建成功!","request_id":"d0793ba1-32df-44f1-b5fb-6dbd4ec211a5","task_id":"20250813104545707549754_TASK_REPORT"}
```

### 3.3.2 查询进度
根据返回的 **request_id**，继续根据这个任务ID号查询状态。

```bash
# 获取处理状态
curl http://localhost:8687/v1/progress/<request_id>
```


## 4. Docker
项目提供 docker-compose.yml 方便同时管理项目的环境镜像和Chrome镜像，环境镜像需要实现打包，业务代码通过映射到镜像种的 */app* 文件目录。

### 4.1 创建环境镜像
```bash
# 创建镜像，不含业务代码
docker build -t  leixin/coder-artifacts-dev:latest .
```

###  4.2 Docker compose 启动

``` bash
# 启动服务
docker compose up -d

# 查看容器状态（此时依赖的两个容器应当均为 running）
docker compose ps

# 进入 Python容器测试
docker compose exec leixin-coder-artifacts bash

# 停止容器
docker compose down
```



