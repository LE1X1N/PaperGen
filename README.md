# Pagergen 论文主体生成服务
An automonous pipeline for generating thesis' body.

自动化生成论文主体结构与内容，输入论文题目即可生成可直接编辑的 docx 文档。


## 一、核心功能
- 结构化输出：自动生成「章节正文（docx）、论文目录（JSON）、摘要（JSON） 等」，支持二次开发；  
- 灵活配置：适配不同 LLM 服务（OpenAI API/本地化模型）；  
- 高效生成：支持多线程并发生成，单篇论文平均耗时30s。


## 二、前置准备
### 1. 环境要求
- Python 3.12+  
- LLM 服务访问权限（需配置 API 密钥或本地化模型地址）  
- 依赖包：见 `requirements.txt`

``` bash
git clone git@github.com:LE1X1N/PaperGen.git
cd PaperGen
```

### 2. 安装依赖
```
pip install -r requirements.txt
```

### 3. 配置模型
编辑 `conf/service_config.yaml`，修改openai相关配置：

```yaml
openai:
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    model: qwen3-coder-flash
```


## 三、使用指南

指定论文标题, 生成默认配置的论文主体

``` bash
python app.py --title "基于SpringBoot的网吧管理系统"
```

``` bash
python app.py --title "基于协同过滤算法的电影推荐小程序"
```

``` bash
python app.py --title "基于物联网的智能家居系统设计"
```

``` bash
python app.py --title "网络文学对传统文学的影响"
```

``` bash
python app.py --title "中小企业融资困境与突破路径研究"
```


## 四、效果演示





项目结构：
```
PaperGen
├─ app.py                       # 入口文件
├─ conf 
│  └─ service_config.yaml       # 配置文件
├─ docs
├─ README.md
├─ requirements.txt
└─ src
   ├─ config
   │  └─ __init__.py            # 配置初始化
   ├─ llm
   │  ├─ client.py              # LLM服务器连接
   │  ├─ prompt.py              # 提示词相关
   │  └─ __init__.py
   ├─ service
   │  ├─ content
   │  │  ├─ json_generator.py       # JSON类型内容生成，如目录JSON，需求表格JSON等
   │  │  ├─ section_generator.py    # 纯文本内容生成，支持多线程
   │  │  └─ __init__.py
   │  └─ doc
   │     ├─ doc_composer.py          # 文档组装
   │     ├─ pipeline.py              # 核心流程控制
   │     ├─ style_controller.py      # 风格控制
   │     └─ __init__.py
   └─ utils
      └─ common.py
```