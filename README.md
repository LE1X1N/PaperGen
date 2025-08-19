# 代码界面渲染

## 1. 项目结构

```
coder-artifacts
├─ Dockerfile
├─ README.md
├─ config
│  ├─ config.yaml            # 服务参数，端口
│  └─ dev.yaml               # uWSGI服务器参数
├─ demo                     
│  ├─ app.py                 # 基于Gradio的可视化界面
│  ├─ app_conf.py
│  ├─ app_style.css
│  └─ utils.py
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
├─ static                   # 不同局部的静态jsx模板
│  ├─ 上中下布局
│  ├─ 侧边布局
│  ├─ 小程序
│  └─ 顶部-侧边布局
├─ uwsgi_service.ini
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

``` bash
# 发送请求
curl -X POST http://localhost:8687/v1/gen_images -H "Content-Type: application/json"  -d @data.json
```

此时会立马返回对应的任务ID号，比如：

{"message":"Task launch success!","request_id":"3ca7c636-cd02-4f66-ab01-632431d95978"}


可以根据这个任务ID号查询状态
```bash
# 获取处理状态
curl http://localhost:8687/v1/progress/<request_id>
```

## 5. 镜像启动

```bash
# 创建镜像，不含业务代码
docker build -t  leixin/coder-artifacts-dev:latest .

# 将所有代码挂载并运行镜像
docker run -itd  -v  $(pwd):/app --entrypoint /bin/bash  --network host --name leixin-coder-artifacts-dev leixin/coder-artifacts-dev:latest 
```

