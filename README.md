# 镜像准备

### 1. MongoDB

MongoDB 主要用于存储JSON样式的订单状态。

```bash
# 下载镜像
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/mongo:7.0.12
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/mongo:7.0.12  docker.io/library/mongo:7.0.12
```
### 2. Selenium

Selenium主要用于截屏服务。

```bash
# 下载镜像
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/selenium/standalone-chrome:latest
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/selenium/standalone-chrome:latest  docker.io/selenium/standalone-chrome:latest
```

### 3. Minio

Minio主要用于存储生成的图片和代码

```bash
# 下载镜像
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/minio/minio:RELEASE.2025-09-07T16-13-09Z
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/minio/minio:RELEASE.2025-09-07T16-13-09Z  docker.io/minio/minio:RELEASE.2025-09-07T16-13-09Z
```

### 4. Redis

Redis用于在内存中存储订单状态，加速查询速度



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

推荐使用vLLM本地启动模型
``` bash
vllm serve Qwen2.5-Coder-3B-Instruct --gpu-memory-utilization 0.8 --max-model-len 4096
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

当前服务对外提供三个接口：

- /v1/gen_images
- /v1/progress/{request_id}
- /v1/health

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

### 2.3 检查状态
调用此接口将会触发服务状态检查，包括检查 OpenAI、Selenium、DFS以及MongoDB的连接状态。
- OpenAI：尝试向模型发送 "ping" 信息，等待模型回复，若正确得到返回则判断正常。 
- Selenium: 尝试获取一个Chrome Driver，若Driver正常初始化成功则判断正常。
- DFS：向配置文件当中的 dfs.health_check_url 发送查询状态信息，如返回无错误码则判断正常。
- MongoDB：连接MongoDB，并尝试读取数据库的条目数量，若能够正确返回条目数量则判断正常。

```bash
# 检查当前服务的状态
curl http://localhost:8687/v1/health
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

### 4.1 Mongodb





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


## 5. 问题定位

- **1️⃣ 输出图片样式不满意，怎样修改图片的样式呢？**
  
  生成图片的样式（如上下布局，左右布局，基础样式等）主要由 **/static** 下的不同模板控制，基于此模板模型会生成复合输入JSON描述的对应tsx代码，因此如果产品认为生成图片的样式布局需要调整，可以尝试在 **/static** 下添加或者修改对应的模板tsx代码。

- **2️⃣ 输出图片有些细节问题，比如功能栏位置错误，不美观等**

  基于模板tsx代码，在 **src/llm/prompt.py** 当中将会拼接为对应的模型提示词，有模型生成最终的 tsx代码用于渲染。由于大模型生成内容的不确定性，图片当中可能有些细节无法完全控制（比如：渲染出的界面滚动条太粗）。这个时候就需要调整提示词。在对应的提示词生成函数当中添加 “滚动条限制为5px” 类似的描述，则最终生成的图片细节会有改善。

- **3️⃣ 输出图片比例存在问题 / 图片需要进行裁剪**
  
  当前在 **src/core/task_manager.py** 的第11步当中提供了图片后处理操作。传入初始图像的路径，直接在生成图片上进行操作，比如使用cv2库，进行裁剪或者拉伸操作。

- **4️⃣ 可以添加更多的生成样式吗？**

  当前支持 style为 网页端（0），APP（1），微信小程序（2），分别对应传入JSON的style字段为 0、1、2的情况。当需要扩充样式，则需要在 **src/core/data_processing/tmpl_manager.py** 当中添加对于对应类别的样式解析。比如添加ios (4) 对应 **/static** 目录下的 ios 文件夹。接着对于 **src/llm/prompt.py** 添加对应 style的提示词即可。

- **5️⃣ 我想查看某一个tsx代码的样式调整，怎样做？**

  在 **src/browser/renderer.py** 当中的 **launch_sandbox_demo()** 函数基于gradio在一个浏览器当中渲染tsx代码，将tsx文件读取并传入此函数当中，即可以在浏览器当中输入对应的端口查看渲染情况。

  示例测试代码：

  ``` python
  import os
  import sys

  from src.browser import launch_sandbox_demo

  code = open("static/app/模板2.jsx").read()
  launch_sandbox_demo("111", "222", code, 50049)  # 这里的111， 222随便填写，50049为浏览器端口
  ```
  接着在浏览器当中访问 *http://localhost:50049* 即可查看渲染情况。
  注意：当前 **launch_sandbox_demo()** 当中 demo.launch 参数设置 quiet=True，可以设置为 False方便查看浏览器路径。



## 6. 项目结构

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