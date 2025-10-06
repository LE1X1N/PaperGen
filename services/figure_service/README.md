# Pagergen 论文配图生成服务
An automonous pipeline for generating thesis' figures.


# 1. Prerequisite 🚧

预下载以下项目所依赖的镜像 🐳 。

⚠️：若遇到网络问题，请尝试使用 *swr.cn-north-4.myhuaweicloud.com/ddn-k8s/* 镜像前缀。

- **MongoDB**:主要用于存储JSON样式的订单状态。

  ```bash
  docker pull docker.io/library/mongo:7.0.12
  ```
- **Selenium**: 主要用于截屏服务。

  ```bash
  docker pull docker.io/selenium/standalone-chrome:latest
  ```

- **Minio**: 用于存储生成的图片和代码

  ```bash
  docker docker.io/minio/minio:RELEASE.2025-09-07T16-13-09Z
  ```

- **Redis**: 用于在内存中存储订单状态，加速查询速度





# 2. 配置文件修改 🔧

服务依赖代码模型生成对应的前端代码，并且依赖 selenium/standalone-chrome 镜像作为浏览器访问代理，提供的 selenium+webdriver+headless 浏览器的截屏功能。

## 2.1 LLM服务商配置
根据所调用大模型的服务商，修改 **docker/.env** 当中对应OpenAI的相关配置

```bash
# OpenAI config
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen3-coder-480b-a35b-instruct
```

推荐使用vLLM本地启动模型
``` bash
vllm serve Qwen2.5-Coder-3B-Instruct --gpu-memory-utilization 0.8 --max-model-len 4096
```

## 2.2 服务内部线程池大小
线程池大小决定服务内部同一时间能够处理的最大任务数量。比如同一个时间收到10个api请求，每个请求内部包括15个图片生成需求，则此时并发应当对应150个任务处理线程。

根据业务需求修改**config/service_config.yaml** 当中的线程配置：

``` yaml
# service config
max_workers: 150          # multithread
```

## 2.3 Chrome Driver的sessions数量
对于每一张图片均需要单独在Selenium中初始化一个Chrome Driver，对应于启动一个浏览器渲染代码。每个浏览器进程（如 Chrome）启动后约占用 200-500MB 内存。因此单结点的承载driver数量受限于server的内存和CPU核心数量。即虽然配置了线程池，但是线程之间仍然会争抢配置的有限个Driver。

根据业务需求，修改 **docker/.env** 中的Seleium配置：

``` bash
# Selenium config
SE_NODE_MAX_SESSIONS=5    # <- Make it larger!
```


#  3. Service Interface / API 🌐

当前服务对外提供三个接口：

- /v1/gen_figures
- /v1/progress/{request_id}
- /v1/health

具体的接口请参考 [接口文档](docs/接口文档.md)

## 3.1 生成请求

- **/v1/gen_figures**

``` bash
# 发送请求
curl -X POST http://localhost:8686/v1/gen_figures -H "Content-Type: application/json"  -d @docs/测试输入JSON/app/基于Android的背单词系统设计与实现.json
```

此时会立马返回对应的任务ID号，如下所示。其中 **request_id** 为系统自动为本次请求创建的唯一ID，后续可基于此ID查询任务进度。

``` bash
{"code":0,"message":"任务创建成功!","request_id":"d0793ba1-32df-44f1-b5fb-6dbd4ec211a5","task_id":"20250813104545707549754_TASK_REPORT"}
```

## 3.2 查询进度
- **/v1/progress/{request_id}**

根据返回的 **request_id**，继续根据这个任务ID号查询状态。

```bash
# 获取处理状态
curl http://localhost:8687/v1/progress/<request_id>
```

## 3.3 检查状态
- **/v1/health**

调用此接口将会触发服务状态检查，包括检查 OpenAI、Selenium、DFS以及MongoDB的连接状态。
- OpenAI：尝试向模型发送 "ping" 信息，等待模型回复，若正确得到返回则判断正常。 
- Selenium: 尝试获取一个Chrome Driver，若Driver正常初始化成功则判断正常。
- DFS：向配置文件当中的 dfs.health_check_url 发送查询状态信息，如返回无错误码则判断正常。
- MongoDB：连接MongoDB，并尝试读取数据库的条目数量，若能够正确返回条目数量则判断正常。

```bash
# 检查当前服务的状态
curl http://localhost:8687/v1/health
```

# 4. Quick Start 🚀

项目提供 docker-compose.yml 方便同时管理项目的环境镜像和Chrome镜像，环境镜像需要实现打包，业务代码通过映射到镜像中的 */app* 文件目录。

## 4.1 创建环境镜像

```bash
# 创建镜像，业务代码通过映射得到
docker compose build
```

## 4.2 镜像启动

``` bash
# 启动服务
docker compose up -d

# 查看容器状态（此时依赖的两个容器应当均为 running）
docker compose ps

# 进入容器
docker compose exec leixin-coder-artifacts bash
```

## 4.3 服务启动
``` bash
uwsgi --ini uwsgi_service.ini # 适用于生产环境提供多进程
# 或
python wsgi.py    # 适用于测试环境单进程调试
```

## 4.4 服务停止
``` bash
# 停止容器
docker compose down
```


# 5. 问题定位 🐛

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

  from src.infrastructure.browser import launch_sandbox_demo

  code = open("static/app/模板2.jsx").read()
  launch_sandbox_demo("111", "222", code, 50049)  # 这里的111， 222随便填写，50049为浏览器端口
  ```
  接着在浏览器当中访问 *http://localhost:50049* 即可查看渲染情况。
  注意：当前 **launch_sandbox_demo()** 当中 demo.launch 参数设置 quiet=True，可以设置为 False方便查看浏览器路径。



# 6. 项目结构 🏠

```
PaperGen-Figure-Service
├─ Dockerfile
├─ README.md
├─ conf
│  └─ service_config.yaml 
├─ docs
│  ├─ 接口文档.md
│  ├─ 测试输入JSON
│  │  ├─ app              # APP类型测试输入
│  │  ├─ web              # 网站类型测试输入
│  │  └─ wechat           # 微信小程序类型测试输入
│  └─ 测试返回.json
├─ requirements.txt
├─ src
│  ├─ api
│  │  ├─ __init__.py
│  │  ├─ routes.py              # API 接口
│  │  └─ validator
│  │     └─ json_validator.py   # 输入JSON正确性判断
│  ├─ app.py                    # Flask app初始化  
│  ├─ config
│  │  ├─ __init__.py
│  │  └─ loader.py          # 配置文件加载
│  ├─ domain
│  │  └─ services
│  │  │  ├─ __init__.py
│  │  │  ├─ data_parser.py  # 输入解析为module与page任务
│  │  │  ├─ prompts.py      # prompt相关
│  │  │  └─ tmpl_parser.py  # 模板解析
│  │  └─ pipeline.py        # 任务核心，负责拆解与执行任务
│  ├─ errors.py
│  ├─ infrastructure
│  │  ├─ browser
│  │  │  ├─ __init__.py
│  │  │  ├─ manager.py           # Selenium 负责截屏逻辑
│  │  ├─ db
│  │  │  ├─ __init__.py
│  │  │  └─ client.py            # MongoDB 相关，连接，插入等
│  │  ├─ llm
│  │  │  ├─ __init__.py
│  │  │  ├─ client.py            # LLM 相关，建立连接
│  │  ├─ renderer
│  │  │  ├─ __init__.py
│  │  │  └─ gradio_renderer.py   # Gradio渲染
│  │  └─ storage                
│  │     ├─ __init__.py
│  │     └─ local_storage.py     # 本地存储，管理代码和图片的本地存储(screenshot/) 
│  │     └─ minio_storage.py     # MinIO存储，管理代码和图片S3存储
│  ├─ repository
│  │  └─ progress_repository.py  # 流程控制，处理状态JSON保存至MongoDB
│  │  ├─ storage_factory.py      # 存储工厂，根据配置决定实例化minio/local
│  │  └─ storage_repository.py   # storage抽象层
│  └─ utils
│     ├─ __init__.py
│     ├─ common.py
│     ├─ image_utils.py
│     └─ logger.py
├─ static                # 存放不同类型jsx模板代码 
│  ├─ app
│  ├─ web
│  └─ wechat
├─ uwsgi_service.ini     # uwsgi 配置文件
└─ wsgi.py               # 服务入口
```
