# 代码界面渲染

## 1. 项目结构

```
Coder-Artifacts
├─ README.md
├─ config
│  ├─ __init__.py
│  ├─ system_conf.yaml     # 服务参数，端口
│  └─ uwsgi_service.ini    # uWSGI服务器参数
├─ demo                    # 基于Gradio的demo
│  ├─ app.py
│  ├─ app_conf.py
│  └─ app_style.css
├─ requirements.txt
├─ src
│  ├─ __init__.py
│  ├─ api
│  │  └─ routes.py         # API
│  ├─ app.py               # Flask app初始化
│  ├─ browser
│  │  ├─ __init__.py
│  │  ├─ manager.py       # Selenium Driver相关
│  │  └─ renderer.py      # Gradio界面渲染相关
│  ├─ core
│  │  ├─ parser.py        # JSON解析
│  │  └─ task_manager.py  # 任务处理核心
│  ├─ errors.py           
│  ├─ llm
│  │  ├─ __init__.py
│  │  └─ client.py        # LLM调用
│  ├─ tmpl
│  │  ├─ __init__.py
│  │  ├─ static
│  │  │  ├─ 小程序模板.jsx
│  │  │  ├─ 网页模板-管理系统（上下）.jsx
│  │  │  └─ 网页模板-管理系统（左右）.jsx
│  │  └─ tmpl_manager.py  # 代码模板管理
│  └─ utils
│     ├─ __init__.py
│     ├─ common.py
│     └─ logger.py
└─ wsgi.py

```


## 2. Demo测试

基于gradio的可视化界面渲染流程Demo。

```shell
# 启动前端可视化界面
python launch_app.py
```


## 3. 服务启动

依赖 selenium/standalone-chrome 镜像作为浏览器访问代理，提供了全套 selenium+webdriver+headless 浏览器的功能

### 3.1 代码模型启动

``` bash

CUDA_VISIBLE_DEVICES=2,3 vllm serve ~/huggingface/Qwen3-Coder-30B-A3B-Instruct/  --port 8001  --gpu-memory-utilization 0.90  --served-model-name Qwen3 --enable_chunked_prefill --enable_prefix_caching

```

### 3.2 Selenium容器启动
``` bash
# 启动
docker run -d --network host --name leixin-selenium-chrome selenium/standalone-chrome

# 停止 
docker stop selenium-chrome
docker rm selenium-chrome
```

### 3.2 提供API服务
使用uwsgi / Flask 提供接口服务
``` bash
# 启动
uwsgi --ini config/uwsgi_service.ini

# 停止
uwsgi --stop log/uwsgi.pid
```

## 4. 服务测试

```
curl -X POST http://localhost:8687/v1/gen_images -H "Content-Type: application/json"  -d @data.json
```



